This is the expected script for the prototype Prototypes\nebula-loginnew.png

And for this script especially, I created a debug system [WIP] with the following: (removed)

- Messages: blue color
- Warning: yellow color
- Error: red color

Messages:
Loaded assets: ```[MESSAGE] Asset [bold: {asset-dir}] has been loaded.```

Button clicked: ```[MESSAGE] Button [bold: {button-name}] has been clicked.```

Network connection established: ```"[MESSAGE] Network connection established successfully to network [bold: {network-name}]"```

Warnings:
Asset not found: ```[WARNING] Asset [bold: {asset-dir}] is not found, needed for [bold: {button-name or image}]```

Shell Execution errors: ```[WARNING] ShellExecute 'message' failed.```

Network connection not established: ```"[WARNING] Network connection could not be established."```

High CPU usage: ```"[WARNING] High CPU usage detected: [bold:{cpu_usage}%]."```

Memory leak detected: ```"[WARNING] Possible memory leak detected."```

Errors:
Critical error: ```"[ERROR] Critical error: [bold:{error_message}]. Program will now exit."```

Fatal error: ```"[ERROR] Fatal error: [bold:{error_message}]. Program cannot continue."```

Unhandled exception: ```"[ERROR] Unhandled exception: [bold:{exception_type}]: [bold:{exception_message}]."```
Invalid input: ```"[ERROR] Invalid input: [bold:{input_value}]."```

Timeout: ```"[ERROR] Operation timed out."```

File system error: ```"[ERROR] File system error: [bold:{error_message}]."```

Network error: ```"[ERROR] Network error: [bold:{error_message}]."```

for the shellexecution part, what i mean by message is the # for example in this:
```ShellExecute '#' failed (error 2).```
