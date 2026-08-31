<#
    Minimal MCP-compliant stdio calculator server.
    Speaks newline-delimited JSON-RPC 2.0 per the Model Context Protocol stdio transport.
    Exposes a single tool: "calculate", which evaluates a basic arithmetic expression.
#>

$ErrorActionPreference = 'Stop'

$stdout = [Console]::Out
$stdin = [Console]::In

function Send-Message {
    param($Object)
    $json = $Object | ConvertTo-Json -Depth 10 -Compress
    $stdout.WriteLine($json)
    $stdout.Flush()
}

function Invoke-Calculation {
    param([string]$Expression)

    # Only allow digits, whitespace, and basic arithmetic operators/parentheses — no arbitrary code execution.
    if ($Expression -notmatch '^[0-9\.\s\+\-\*\/\(\)]+$') {
        throw "Expression contains unsupported characters."
    }

    $table = New-Object System.Data.DataTable
    return $table.Compute($Expression, $null)
}

while ($true) {
    $line = $stdin.ReadLine()
    if ($null -eq $line) { break }
    if ([string]::IsNullOrWhiteSpace($line)) { continue }

    try {
        $request = $line | ConvertFrom-Json
    } catch {
        continue
    }

    $method = $request.method
    $id = $request.id

    switch ($method) {
        'initialize' {
            Send-Message @{
                jsonrpc = '2.0'
                id      = $id
                result  = @{
                    protocolVersion = '2024-11-05'
                    capabilities    = @{ tools = @{} }
                    serverInfo      = @{ name = 'calculate-windows'; version = '1.0.0' }
                }
            }
        }
        'notifications/initialized' {
            # Notification only — no response required.
        }
        'tools/list' {
            Send-Message @{
                jsonrpc = '2.0'
                id      = $id
                result  = @{
                    tools = @(
                        @{
                            name        = 'calculate'
                            description = 'Evaluates a basic arithmetic expression (+, -, *, /, parentheses).'
                            inputSchema = @{
                                type       = 'object'
                                properties = @{
                                    expression = @{ type = 'string'; description = 'Arithmetic expression, e.g. "2 + 3 * 4".' }
                                }
                                required   = @('expression')
                            }
                        }
                    )
                }
            }
        }
        'tools/call' {
            $toolName = $request.params.name
            $toolArgs = $request.params.arguments
            if ($toolName -eq 'calculate') {
                try {
                    $result = Invoke-Calculation -Expression ([string]$toolArgs.expression)
                    Send-Message @{
                        jsonrpc = '2.0'
                        id      = $id
                        result  = @{
                            content = @(
                                @{ type = 'text'; text = [string]$result }
                            )
                        }
                    }
                } catch {
                    Send-Message @{
                        jsonrpc = '2.0'
                        id      = $id
                        result  = @{
                            content = @(
                                @{ type = 'text'; text = "Error: $($_.Exception.Message)" }
                            )
                            isError = $true
                        }
                    }
                }
            } else {
                Send-Message @{
                    jsonrpc = '2.0'
                    id      = $id
                    error   = @{ code = -32601; message = "Unknown tool: $toolName" }
                }
            }
        }
        'ping' {
            Send-Message @{
                jsonrpc = '2.0'
                id      = $id
                result  = @{}
            }
        }
        default {
            if ($null -ne $id) {
                Send-Message @{
                    jsonrpc = '2.0'
                    id      = $id
                    error   = @{ code = -32601; message = "Method not found: $method" }
                }
            }
        }
    }
}
