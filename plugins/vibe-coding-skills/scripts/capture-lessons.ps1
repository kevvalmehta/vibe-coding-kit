# capture-lessons.ps1 -- the "learning hook"
#
# Runs on Claude Code's Stop event (after every turn). Scans the conversation
# for signs the user corrected the AI or stated a rule, and appends a CANDIDATE
# lesson to .specify/memory/lessons.md (the Scar Log) for later review.
#
# WHY a hook, not a skill: a hook fires 100% of the time; a skill is probabilistic.
# WHY only "candidates": a script can't UNDERSTAND a lesson, only flag suspects by
# keyword. A human (or Claude) promotes a good candidate into a real L-# entry.
#
# Contract: opt-in (no-op unless lessons.md exists), append-only, and it must NEVER
# break a session -- any error is swallowed and the script exits 0.
#
# NOTE: keep this file ASCII-only. Windows PowerShell 5.1 reads a BOM-less UTF-8
# script as ANSI, which corrupts smart punctuation and breaks the parser.

[CmdletBinding()]
param(
    # For testing: pass the hook JSON directly instead of reading stdin.
    [string]$StdinJson
)

$ErrorActionPreference = 'Stop'

# Phrases that suggest a correction happened or a rule emerged. Case-insensitive.
$SignalPatterns = @(
    "\bno,?\s+(actually|wait|don't|do not)\b",
    "\bthat'?s\s+(wrong|not right|incorrect)\b",
    "\bdon'?t\s+do\s+that\b",
    "\bstop\s+doing\b",
    "\bfrom now on\b",
    "\b(you|that|it)\s+broke\b",
    "\brevert\b",
    "\bundo\s+(that|this|it)\b",
    "\bnever\s+(do|use|touch|add|change)\b",
    "\balways\s+(do|use|run|check)\b",
    "\bwhy did you\b",
    "\bnot what i\s+(asked|wanted|meant)\b",
    "\byou (shouldn'?t|should not)\b"
)

function Get-UserText {
    # Pull the real typed text out of one transcript line; ignore tool results,
    # and strip hook-injected <system-reminder> blocks so we only scan what the user wrote.
    param($Line)
    $obj = $null
    try { $obj = $Line | ConvertFrom-Json } catch { return $null }
    if ($null -eq $obj -or $obj.type -ne 'user') { return $null }
    $content = $obj.message.content
    if ($null -eq $content) { return $null }

    $text = ''
    if ($content -is [string]) {
        $text = $content
    } else {
        foreach ($block in $content) {
            if ($block.type -eq 'text' -and $block.text) { $text += "`n" + $block.text }
            # tool_result / tool_use blocks are deliberately skipped
        }
    }
    if ([string]::IsNullOrWhiteSpace($text)) { return $null }

    # Drop injected context so it can't trip the scanner.
    $text = [regex]::Replace($text, '(?s)<system-reminder>.*?</system-reminder>', ' ')
    $text = ($text -replace '\s+', ' ').Trim()
    if ([string]::IsNullOrWhiteSpace($text)) { return $null }
    return $text
}

function Invoke-LessonCapture {
    param([string]$Json)

    $hook = $Json | ConvertFrom-Json
    $cwd = $hook.cwd
    $transcript = $hook.transcript_path
    $sessionId = $hook.session_id
    if (-not $cwd) { $cwd = (Get-Location).Path }

    $lessonsPath = Join-Path $cwd '.specify\memory\lessons.md'
    if (-not (Test-Path $lessonsPath)) { return }          # opt-in: no Scar Log, no-op
    if (-not $transcript -or -not (Test-Path $transcript)) { return }

    $statePath = Join-Path $cwd '.specify\memory\.lessons-state.json'
    $state = @{}
    if (Test-Path $statePath) {
        try {
            $raw = Get-Content $statePath -Raw | ConvertFrom-Json
            foreach ($p in $raw.PSObject.Properties) { $state[$p.Name] = [int]$p.Value }
        } catch { $state = @{} }
    }

    # -Encoding UTF8 both reads: PS 5.1 defaults to ANSI on BOM-less files, which
    # garbled em-dashes ("a-hat-euro" mojibake) AND broke the dedup comparison below.
    $lines = @(Get-Content $transcript -Encoding UTF8)
    $total = $lines.Count
    $startIdx = 0
    if ($sessionId -and $state.ContainsKey($sessionId)) { $startIdx = [int]$state[$sessionId] }
    if ($startIdx -lt 0) { $startIdx = 0 }

    $existing = Get-Content $lessonsPath -Raw -Encoding UTF8
    # Dedup on letters+digits only: encoding garble mangles punctuation, never alnum,
    # so this also matches entries the pre-fix version already wrote garbled.
    $existingKey = ($existing -replace '[^a-zA-Z0-9]', '').ToLowerInvariant()
    $found = New-Object System.Collections.Generic.List[string]
    $foundKeys = New-Object System.Collections.Generic.List[string]

    for ($i = $startIdx; $i -lt $total; $i++) {
        $userText = Get-UserText -Line $lines[$i]
        if (-not $userText) { continue }
        foreach ($pat in $SignalPatterns) {
            if ($userText -imatch $pat) {
                $phrase = $userText
                if ($phrase.Length -gt 200) { $phrase = $phrase.Substring(0, 200) + '...' }
                # de-dupe: skip if this phrase is already in the file or this batch
                $key = ($phrase -replace '[^a-zA-Z0-9]', '').ToLowerInvariant()
                if ($key.Length -gt 80) { $key = $key.Substring(0, 80) }
                if (-not $key -or $existingKey.Contains($key) -or $foundKeys.Contains($key)) { break }
                $found.Add($phrase)
                $foundKeys.Add($key)
                break   # one candidate per message is enough
            }
        }
    }

    if ($found.Count -gt 0) {
        $sb = New-Object System.Text.StringBuilder
        if (-not $existing.Contains('## Candidate lessons')) {
            [void]$sb.AppendLine()
            [void]$sb.AppendLine('---')
            [void]$sb.AppendLine()
            [void]$sb.AppendLine('## Candidate lessons (auto-captured -- review, then promote to an L-# entry or delete)')
            [void]$sb.AppendLine()
            [void]$sb.AppendLine('<!-- The learning hook (scripts/capture-lessons.ps1) appends suspects here when it')
            [void]$sb.AppendLine('     sees you correct the AI or state a rule. These are NOT confirmed lessons.')
            [void]$sb.AppendLine('     Confirm a good one by writing it up as an L-# entry above, then delete it here. -->')
        }
        $stamp = (Get-Date -Format 'yyyy-MM-dd HH:mm')
        $cleanId = ($sessionId -replace '[^a-zA-Z0-9]', '')
        $shortId = if ($cleanId) { $cleanId.Substring(0, [Math]::Min(6, $cleanId.Length)) } else { 'unknown' }
        foreach ($phrase in $found) {
            [void]$sb.AppendLine()
            [void]$sb.AppendLine("### candidate -- $stamp (session $shortId)")
            [void]$sb.AppendLine("**Trigger phrase (you said):** ""$phrase""")
            [void]$sb.AppendLine('**Action:** review, then promote to an L-# entry above, or delete.')
        }
        Add-Content -Path $lessonsPath -Value $sb.ToString() -Encoding UTF8
    }

    # remember how far we scanned so re-runs don't duplicate
    $state[$sessionId] = $total
    ($state | ConvertTo-Json -Compress) | Set-Content -Path $statePath -Encoding UTF8
}

try {
    if (-not $StdinJson) { $StdinJson = [Console]::In.ReadToEnd() }
    if ($StdinJson) { Invoke-LessonCapture -Json $StdinJson }
} catch {
    # A hook must never break a session. Swallow and exit clean.
}
exit 0
