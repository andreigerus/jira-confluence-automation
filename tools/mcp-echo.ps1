<#
    Minimal MCP-compliant stdio echo server.
    Speaks newline-delimited JSON-RPC 2.0 per the Model Context Protocol stdio transport.
    Exposes two tools: "echo" (returns back the "message" argument) and "get_time" (returns the current local time).
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
                    serverInfo      = @{ name = 'echo-windows'; version = '1.0.0' }
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
                            name        = 'echo'
                            description = 'Echoes back the provided message.'
                            inputSchema = @{
                                type       = 'object'
                                properties = @{
                                    message = @{ type = 'string'; description = 'Text to echo back.' }
                                }
                                required   = @('message')
                            }
                        }
                        @{
                            name        = 'get_time'
                            description = 'Returns the current local date and time.'
                            inputSchema = @{
                                type       = 'object'
                                properties = @{}
                            }
                        }
                    )
                }
            }
        }
        'tools/call' {
            $toolName = $request.params.name
            $toolArgs = $request.params.arguments
            if ($toolName -eq 'echo') {
                Send-Message @{
                    jsonrpc = '2.0'
                    id      = $id
                    result  = @{
                        content = @(
                            @{ type = 'text'; text = [string]$toolArgs.message }
                        )
                    }
                }
            } elseif ($toolName -eq 'get_time') {
                Send-Message @{
                    jsonrpc = '2.0'
                    id      = $id
                    result  = @{
                        content = @(
                            @{ type = 'text'; text = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss') }
                        )
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
