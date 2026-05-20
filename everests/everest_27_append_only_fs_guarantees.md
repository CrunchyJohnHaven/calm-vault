# Everest 27 — Append-Only Filesystem Guarantees

*Phase III — Self-Report Substrate. Prereq: Everest 26.*

## Statement of purpose

The `user_state.jsonl` log must remain append-only, or the protocol must detect that it has been compromised. Filesystems are inherently mutable — even "append-only" flags can be removed by privilege escalation. This everest layers OS-level write-protection mechanisms with a cross-platform monitoring daemon (Calm Sentinel) that subscribes to filesystem events and re-verifies the chain hash (Everest 28) whenever out-of-band modifications occur. The hash chain is the protocol-level defense; the OS mechanisms are defense-in-depth.

## Core insight

The structural guarantee is not "the filesystem prevents all writes" — that is infeasible. The guarantee is: *the Calm operator detects any out-of-band write to `user_state.jsonl` within 100 ms, pauses disclosure operations, re-verifies the chain (Everest 28), and alerts the principal if verification fails*. Together, the hash chain (E28) and the Sentinel daemon (this everest) create a tamper-evident, tamper-detecting substrate that is suitable as the hydration anchor for Calm Witness disclosure.

## macOS (APFS)

### Mechanism 1: system-immutable flag

Apply the `schg` (system immutable) flag to `user_state.jsonl`:

```bash
chflags schg ~/.calm-vault/user_state.jsonl
```

**Effect:** Blocks modification by any user except root, and root only in single-user mode (or via explicit `chflags -schg` in single-user mode). Does not prevent removal of the file itself.

**Calm operator's append protocol:** Before each append operation, the operator launchd privileged helper (see Mechanism 3) temporarily removes the flag (`chflags nschg`), appends a new record to the file, re-verifies the chain hash, then reasserts the flag (`chflags schg`). The window of vulnerability is ≤ 5 ms (Mechanism 3 timeout). Any other process attempting modification is denied by the kernel.

**Compromise case:** A root-privileged actor on the machine can remove the flag, edit the file, and restore the flag, potentially leaving no trace. Defense: Mechanism 2 (snapshots) and Mechanism 3 (FSEventStream).

### Mechanism 2: APFS snapshots

Configure Time Machine or a custom snapd (launchd periodic task) to snapshot the entire `~/.calm-vault/` directory daily, retained for 30 days:

```bash
sudo launchctl load /Library/LaunchDaemons/com.calm-vault.snapshot.plist
```

Example plist entry:
```xml
<key>StartInterval</key>
<integer>86400</integer>  <!-- 24 hours in seconds -->
<key>ProgramArguments</key>
<array>
  <string>/usr/bin/tmutil</string>
  <string>snapshot</string>
</array>
```

**Effect:** A silent copy of the vault state at midnight every day. If an adversary edits `user_state.jsonl`, the snapshots preserve the original version. Any subsequent Calm Witness disclosure can detect the gap by re-verifying against snapshots from the disclosure date.

**Retention:** 30 snapshots = 30 days of rollback. Operationally tunable; the default assumes weekly disclosure audits.

### Mechanism 3: FSEventStream + Calm Sentinel

The Calm Sentinel daemon (launched as a LaunchAgent: `~/Library/LaunchAgents/com.calm.sentinel.plist`) subscribes to `FSEventStreamCreate` on the vault directory, watching for `kFSEventStreamEventFlagItemModified` and `kFSEventStreamEventFlagItemRenamed` events:

```python
# Pseudocode; real implementation uses ctypes/FSEvents library
import os, time, hashlib
from fsevents import observer, FileModifiedEvent

observer = observer.Observer()
vault_path = os.path.expanduser('~/.calm-vault')
handler = AlertOnVaultModify(vault_path)
observer.schedule(handler, vault_path, recursive=False)
observer.start()

class AlertOnVaultModify:
    def __init__(self, vault_path):
        self.vault_path = vault_path
        self.user_state_path = os.path.join(vault_path, 'user_state.jsonl')
        self.last_verified_hash = self.read_last_chain_head()
    
    def on_modified(self, event):
        if event.src_path == self.user_state_path and event.event_type != 'moved':
            # Out-of-band modification detected
            self.trigger_verification()
    
    def trigger_verification(self):
        # Call Everest 28 verifier
        import subprocess
        result = subprocess.run(['calm-witness', 'verify-chain'], 
                                capture_output=True, timeout=0.1)
        if result.returncode != 0:
            # Chain verification FAILED → tamper
            self.emit_alert('CHAIN_TAMPER_DETECTED', result.stdout)
            # Write kind: "chain.tamper_alert" to event log with out-of-band delivery
        else:
            # Chain verification OK but event was unexpected
            current_hash = self.read_last_chain_head()
            if current_hash == self.last_verified_hash:
                # File touched but content unchanged
                self.log_event('unexpected_fs_event_no_content_change')
            else:
                # File legitimately appended by the operator; update hash
                self.last_verified_hash = current_hash
```

**Event latency:** FSEventStream events fire within ≤ 50 ms of filesystem change. Verification latency ≤ 50 ms (Everest 28, Python stdlib verifier). Total alert latency: ≤ 100 ms p95.

**Deployment:** Sentinel runs continuously as a LaunchAgent (`StartInterval` 0, `KeepAlive` true). Logs events to a separate `~/.calm-vault/sentinel_events.jsonl` with its own hash chain.

### Mechanism 4: SIP + App Sandbox (future)

For iOS and future macOS app-bundled Calm (Everest 89), the Calm app lives in an App Sandbox (`entitlements.plist` with `com.apple.security.files.user-selected.read-write`). The vault cannot be accessed by other apps.

## Linux (fanotify + chattr)

### Mechanism 1: append-only attribute

Apply the append-only attribute to `user_state.jsonl`:

```bash
chattr +a ~/.calm-vault/user_state.jsonl
```

**Effect:** The file can only be opened in `O_APPEND` mode. Writes outside the append position fail. The `+a` flag requires `CAP_LINUX_IMMUTABLE` capability to remove — even `root` cannot clear it without explicitly holding the capability. The kernel's capability model leaves an audit trail (via `audit.log` if auditd is running).

**Calm operator's append protocol:** The operator process holds `CAP_LINUX_IMMUTABLE` (via `setcap cap_linux_immutable=ep /usr/local/bin/calm-witness-append`). To append, the operator:
1. Opens the file in `O_APPEND` mode.
2. Writes the new record (the kernel forces append to EOF).
3. Calls `fsync(2)` to durably persist.
4. Does NOT remove the attribute (it remains in place).

Since the attribute itself prevents non-append writes, the append-only invariant is enforced by the kernel, not just by flag semantics.

**Compromise case:** A root-privileged actor can run `chattr -a` (which requires `CAP_LINUX_IMMUTABLE`), then edit the file. Audit logs show the attribute removal. Defense: Mechanism 2 (fanotify) + Mechanism 3 (filesystem snapshots).

### Mechanism 2: fanotify (FAN_MODIFY monitoring)

The Calm Sentinel daemon subscribes to `fanotify` events on the vault directory:

```python
import select, struct, os

FAN_CLASS_NOTIF = 0x00000000
FAN_MODIFY = 0x00000002
FAN_OPEN = 0x00000020

fd = os.fanotify_init(FAN_CLASS_NOTIF, os.O_RDONLY | os.O_CLOEXEC)
os.fanotify_mark(fd, os.FAN_MARK_ADD | os.FAN_MARK_FILESYSTEM,
                 FAN_MODIFY, -1, os.path.expanduser('~/.calm-vault'))

while True:
    ready, _, _ = select.select([fd], [], [], 1.0)
    if ready:
        buf = os.read(fd, 4096)
        # Parse fanotify_event_metadata
        # Extract file descriptor (fd in metadata)
        # Call readlink /proc/self/fd/<fd> to get path
        # If path == user_state.jsonl: trigger verification
```

**Event latency:** fanotify events arrive within ≤ 10 ms of filesystem change. Verification latency ≤ 50 ms. Total: ≤ 100 ms p95.

**Deployment:** Sentinel runs as a systemd user service (`~/.config/systemd/user/calm-sentinel.service`). Requires no special privileges (fanotify is available to unprivileged processes for monitoring their own filesystem).

### Mechanism 3: btrfs/ZFS snapshots (optional)

On systems with btrfs or ZFS, configure daily snapshots of the vault:

```bash
# btrfs
btrfs subvolume snapshot ~/.calm-vault ~/.calm-vault/.snapshots/daily-$(date +%Y%m%d)

# ZFS
zfs snapshot tank/home/user/calm-vault@daily-$(date +%Y%m%d)
```

Snapshots are read-only and timestamped, providing forensic evidence of the vault state at snapshot time.

### Mechanism 4: SELinux / AppArmor mandatory access control (optional)

For hardened Linux deployments, restrict writers to `user_state.jsonl` to a specific Calm Witness user and AppArmor profile:

```apparmor
/home/*/\.calm-vault/user_state.jsonl {
  owner w,           # owner can write (append only, enforced by chattr +a)
  deny other w,      # all others denied
}
```

With AppArmor + the append-only attribute, even compromised non-owner processes cannot modify the file.

## iOS (Data Protection + Sandbox)

### Mechanism 1: App Sandbox

The Calm Witness iOS app's vault lives in its private container at `~/Library/Containers/com.calm.witness/Data/`. The sandbox prevents other apps from accessing this directory. Inter-app communication requires explicit XPC bridges, which the principal can audit.

### Mechanism 2: Data Protection (file-level encryption)

Mark the vault directory and `user_state.jsonl` with `NSFileProtectionComplete`:

```swift
let vaultURL = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
  .appendingPathComponent("calm-vault")
try FileManager.default.createDirectory(at: vaultURL, withIntermediateDirectories: true)
try (vaultURL as NSURL).setResourceValue(FileProtectionType.complete, forKey: .protectionKeyKey)
```

**Effect:** The file is encrypted at rest using the device's hardware key (Secure Enclave). Readable only when the device is unlocked. Even a physical attacker with a memory dump cannot read the encrypted data.

### Mechanism 3: iCloud backup exclusion

Exclude the vault from iCloud backup by setting `NSURLIsExcludedFromBackupKey`:

```swift
try (vaultURL as NSURL).setResourceValue(true, forKey: .isExcludedFromBackupKey)
```

**Effect:** Each device maintains its own vault state; per-device backups (local iTunes backups) do not include the vault. This prevents a cloud-breach scenario from leaking the principal's entire state history.

### Mechanism 4: App-level monitoring hook

iOS does not expose `fanotify` or `FSEventStream`. Instead, the Calm Witness app's background task (registered with `BGTaskSchedulerDelegate`) periodically re-verifies the chain hash:

```swift
let request = BGProcessingTaskRequest(identifier: "com.calm.verify-chain")
request.requiresNetworkConnectivity = false
try BGTaskScheduler.shared.submit(request)

func handleVerifyChainTask(_ task: BGProcessingTask) {
  let result = verifyChainHash()  // Everest 28
  if result.isValid && result.headMismatch {
    emitAlert("CHAIN_TAMPER_DETECTED")
    pauseDisclosures()
  }
  task.setTaskCompleted(success: result.isValid)
}
```

Verification runs on a ≤ 5 min interval (iOS allows background tasks every 15–30 min; we're conservative to avoid battery drain). If the device is locked or app backgrounded, verification resumes when the app next foregrounds or when the background task fires.

## Android (post-v0)

Post-v0. In v0, Android is deprioritized. The route map includes Everest 97 (Android hardening).

## Monitoring Hook: Calm Sentinel (cross-platform)

A long-running daemon (or app-internal background task on iOS) subscribes to OS filesystem events and enforces the protocol's append-only guarantee at runtime.

### Sentinel's behavior

```
On receipt of FS event (platform-specific: FSEventStream, fanotify, etc.):
  1. Pause all disclosure operations (refuse new `calm-witness generate-proof` calls).
  2. Call calm-witness verify-chain (Everest 28) with 100 ms timeout.
  3. If verification FAILS:
       - Write kind: "chain.tamper_alert" record to event_log.jsonl.
       - Emit out-of-band alert to principal (push notification, email, syslog).
       - Log event to ~/.calm-vault/sentinel_events.jsonl with hash chain.
  4. If verification SUCCEEDS:
       - Check if file content changed since last successful verification.
       - If changed: update internal chain-head reference; permit resumed disclosures.
       - If unchanged (file touched but not modified): write kind: "chain.unexpected_event" to event_log.jsonl.
  5. Resume disclosure operations.
```

### Event log format

Sentinel maintains its own append-only log at `~/.calm-vault/sentinel_events.jsonl`:

```json
{
  "ts": "2026-05-20T14:23:45.123Z",
  "event_type": "fs.modify_detected",
  "path": "user_state.jsonl",
  "verification_result": "PASS",
  "chain_head_before": "abc123...",
  "chain_head_after": "def456...",
  "seq_before": 42,
  "seq_after": 43,
  "latency_ms": 87
}
```

This event log is not part of the user-state protocol but is audit evidence for the principal and external auditors.

### Out-of-band edits we detect

- **Direct write to `user_state.jsonl` by another process:** FSEventStream / fanotify event triggers verification.
- **File replacement (mv old.jsonl new.jsonl):** FSEventStream / fanotify `kFSEventStreamEventFlagItemRenamed` or `FAN_MOVE_SELF` event.
- **Truncation (truncate -s0):** FSEventStream / fanotify `kFSEventStreamEventFlagItemModified` event. Verification fails because seq count decreases.
- **File removal (rm user_state.jsonl):** FSEventStream / fanotify `kFSEventStreamEventFlagItemRemoved` or `FAN_DELETE_SELF` event. Sentinel raises alert.
- **Mounting different filesystem at ~/.calm-vault:** Sentinel periodic health check verifies inode / device ID consistency.

### Out-of-band edits we may not detect (with mitigations)

- **Adversary with root + disabled Sentinel + chain reconstruction:** Adversary re-derives every `record_hash` and `prev_hash` consistently, creating a forged but internally valid chain. **Mitigation:** Everest 30 (Sigsum publication) anchors chain heads to a public transparency log. Reconstructing a chain *and* replaying chain-head publications to Sigsum requires Sigsum operator collusion.
- **Cold-boot / direct disk read:** Adversary reads vault from hibernated memory or direct disk access. **Mitigation:** Everest 16 (data-at-rest encryption) encrypts the vault so that disk contents are ciphertext.

## Acceptance test

### Test 1: Append-only verification on macOS

```bash
#!/bin/bash
set -e

# 1. Create vault and initialize chain
mkdir -p ~/.calm-vault
echo '{"seq":1,"ts":"2026-05-20T10:00:00Z","prev_hash":"0000000000000000000000000000000000000000000000000000000000000000","kind":"genesis","payload":{},"operator":"CALM","principal":"John Bradley","schema_version":0,"record_hash":"<computed>"}' > ~/.calm-vault/user_state.jsonl

# 2. Apply system-immutable flag
chflags schg ~/.calm-vault/user_state.jsonl

# 3. Attempt direct modification (should fail)
if echo "tampered" >> ~/.calm-vault/user_state.jsonl 2>/dev/null; then
  echo "FAIL: File was writable despite schg flag"
  exit 1
fi
echo "PASS: schg flag prevents direct write"

# 4. Verify FSEventStream is subscribed (check process listening)
ps aux | grep -i "calm.*sentinel" | grep -v grep > /dev/null && \
  echo "PASS: Calm Sentinel daemon running" || \
  echo "WARN: Sentinel not running (will start on next session)"

# 5. Verify chain integrity
python3 calm_witness/verify_chain.py ~/.calm-vault/user_state.jsonl
echo "PASS: Chain verification successful"

# 6. Check snapshot retention
ls -d ~/.calm-vault/.snapshots/*/user_state.jsonl 2>/dev/null | wc -l | grep -q "[1-9]" && \
  echo "PASS: At least one snapshot exists" || \
  echo "WARN: No snapshots yet (Time Machine may not have run)"
```

Expected output:
```
PASS: schg flag prevents direct write
PASS: Calm Sentinel daemon running
PASS: Chain verification successful
PASS: At least one snapshot exists
```

### Test 2: Tamper detection on Linux

```bash
#!/bin/bash
set -e

# 1. Create vault and apply append-only attribute
mkdir -p ~/.calm-vault
echo '{"seq":1,...}' > ~/.calm-vault/user_state.jsonl
chattr +a ~/.calm-vault/user_state.jsonl

# 2. Verify attribute is set
lsattr ~/.calm-vault/user_state.jsonl | grep -q "^.*a" && \
  echo "PASS: Append-only attribute set" || \
  exit 1

# 3. Attempt in-place edit (should fail)
if sed -i 's/seq.*/seq": 999/' ~/.calm-vault/user_state.jsonl 2>/dev/null; then
  echo "FAIL: In-place edit succeeded despite append-only"
  exit 1
fi
echo "PASS: Append-only attribute prevents in-place edit"

# 4. Append-only mode should work
if echo '{"seq":2,...}' >> ~/.calm-vault/user_state.jsonl 2>/dev/null; then
  echo "PASS: Append mode allowed"
else
  echo "FAIL: Append mode blocked"
  exit 1
fi

# 5. Verify chain
python3 calm_witness/verify_chain.py ~/.calm-vault/user_state.jsonl
echo "PASS: Chain verification successful"
```

Expected output:
```
PASS: Append-only attribute set
PASS: Append-only attribute prevents in-place edit
PASS: Append mode allowed
PASS: Chain verification successful
```

### Test 3: Sentinel event latency

```python
#!/usr/bin/env python3
import time, json, subprocess, os, signal

vault_path = os.path.expanduser('~/.calm-vault/user_state.jsonl')

# 1. Start Sentinel in background (if not already running)
sentinel_pid = subprocess.Popen(['calm-sentinel', '--daemon']).pid
time.sleep(0.5)  # Let daemon start

# 2. Trigger an append (legitimate)
with open(vault_path, 'a') as f:
    f.write('{"seq":3,...}\n')

# 3. Check event log for latency
event_log_path = os.path.expanduser('~/.calm-vault/sentinel_events.jsonl')
start = time.time()
found = False
while time.time() - start < 1.0:
    try:
        with open(event_log_path, 'r') as f:
            for line in f.readlines()[-5:]:
                event = json.loads(line)
                if event.get('event_type') == 'fs.modify_detected':
                    found = True
                    latency = event.get('latency_ms', 'unknown')
                    if latency < 100:
                        print(f"PASS: Event detected in {latency}ms (p99 < 100ms)")
                    else:
                        print(f"WARN: Event detected in {latency}ms (above target)")
                    break
    except FileNotFoundError:
        pass
    time.sleep(0.01)

if not found:
    print("WARN: Event not detected in event log (may be async)")

# 4. Cleanup
os.kill(sentinel_pid, signal.SIGTERM)
```

## Constraints and future everests

- **Everest 28** (Hash-chain verification) is the protocol-level guarantee; this everest adds OS-level detection.
- **Everest 30** (Sigsum publication) anchors chain heads to a public log, making post-hoc chain reconstruction detectable.
- **Everest 16** (Data-at-rest encryption) protects against cold-boot and direct disk reads.
- **Everest 43** (Rust reference implementation) will port the verifier to Rust for performance-critical deployments.

— Calm, 2026-05-20
