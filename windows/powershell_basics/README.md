# What is Powershell?

>> Powershell is a cross-platform task automation solution made up of a command-line shell, a scripting language & a confirugation management framework. PowerShell runs on Windows, Linux & macOS.

Unlike most shells that only accept and return text, PowerShell accepts and returns .NET objects. The shell includes the following features:
* Robust command-line history
* Tab completion and command prediction
* Supports command and parameter aliases
* Pipeline for chaining commands
* In-console help system, similar to Unix man pages.

Note: The most useful feature for me personally, is the ability to pipe & chain
commands together.

```powershell
# example list the latest 5 files in the current direcory
Get-ChildItem | Sort-Object CreationTime -Descending | Select-Object -First 5

# Output
    Directory: C:\Users\user

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         5/30/2025  11:59 AM             20 .lesshst
d-----         4/25/2025  10:03 AM                .conda
d-----         4/25/2025  10:03 AM                .mamba
d-----         4/25/2025  10:16 AM                micromamba
d-----         4/22/2025  11:49 PM                .nuget
```

## Cmdlets
Powershell uses cmdlets in the `Verb-Noun` Format.
Examples:
```powershell
Get-Process # List running proceses
Get-Service # List all services
Stop-Process -Name notepad # kill notepad process
```
One of the most useful cmdlet is Get-Help with the -Examples options. This will
show you a list of examples of how a cmdlet is used.
```
Get-Help Get-Process -Examples
```
Note you might have to update your help files inorder for this to work.
Run powershell as the administrator & run
```powershell
Update-Help
```

All the cmdlets can have aliases. And powershell has built-in aliases for many
of the cmds in bash & cmd prompt. Example:
* ls & dir both work, aliased to Get-ChildItem
* rm works, aliased to Remove-Item
* cd works, aliased to Set-Location

## Variables & Types
We can define variables as follows:
```powershell
$x = 24 # int
$y = "Diwash" # string
$z = 25.5 # floats

# Arrays in powershell
$colors = @("Red", "Green", "Blue") # array of string
Get-Member -InputObject $colors # print all properties & methods for this list
$colors[1] # accesing the arrays
$colors += "Yellow" # appending to an array

# Dictionary in powershell
$manager = @{"Name"= "Diwash Tamang"; "age"= 40; "marital_status" = "married"} # dictionary / maps
Get-Member -InputObject $colors # print all properties & methods for the dictionary
$manager.Name # getting the value for the key
$manager.Add("Gender", "Male")
```
In powershell, every command returns .NET objects instead of text (Unlike bash).
These variables are objects too. And you can get their types as shown below.

```powershell
$y.GetType()
# OUTPUT
IsPublic IsSerial Name                                     BaseType
-------- -------- ----                                     --------
True     True     String                                   System.Object
```

Here's a list of some useful commands that you can do on a object.
```powershell
Get-Member -InputObject $x # This will list all methods & properties of $x
$x | Select-Object -Property * # piping the object & select all of it's property
Select-Object -InputObject $x -Property * # Same thing as above, but without piping
```

## Logic
PowerShell uses comparison and logical operators for conditions:

- `-eq` (equals), `-ne` (not equals)
- `-gt` (greater than), `-lt` (less than)
- `-ge` (greater or equal), `-le` (less or equal)
- `-and`, `-or`, `-not` for combining conditions

Here's a simple and fun example using comparison logic—let's check how much coffee you have left:

```powershell
$coffeeLevel = 50 # percentage

if ($coffeeLevel -eq 100) {
    Write-Output "Your cup is full! Ready to go."
} elseif ($coffeeLevel -gt 0 -and $coffeeLevel -lt 100) {
    Write-Output "You still have some coffee left. Enjoy your drink!"
} else {
    Write-Output "Oh no, your cup is empty! Time for a refill."
}
```

## Loops
There are multiple ways of writing loops in powershell as shown below:
### 1. `ForEach-Object` (Pipeline Loop)

You can use `ForEach-Object` to process each item in a collection as it passes through the pipeline.

```powershell
1..5 | ForEach-Object { Write-Output "Counting: $_" }
```
_Output:_
```
Counting: 1
Counting: 2
Counting: 3
Counting: 4
Counting: 5
```

### 2. `for` Loop
The classic `for` loop is great for when you need an index.

```powershell
for ($i = 1; $i -le 3; $i++) {
    Write-Output "Rocket launching in $i..."
}
Write-Output "Blast off!"
```
_Output:_
```
Rocket launching in 1...
Rocket launching in 2...
Rocket launching in 3...
Blast off!
```

### 3. `while` Loop

A `while` loop keeps running as long as a condition is true.

```powershell
$energy = 3
while ($energy -gt 0) {
    Write-Output "Dancing! Energy left: $energy"
    $energy--
}
Write-Output "Too tired to dance!"
```
_Output:_
```
Dancing! Energy left: 3
Dancing! Energy left: 2
Dancing! Energy left: 1
Too tired to dance!
```

### 4. `foreach` Loop

The `foreach` loop iterates over each item in a collection.

```powershell
$planets = @("Mercury", "Venus", "Earth")
foreach ($planet in $planets) {
    Write-Output "Welcome to $planet!"
}
```
_Output:_
```
Welcome to Mercury!
Welcome to Venus!
Welcome to Earth!
```

## Functions

Functions in PowerShell let you group code into reusable blocks. You define a function using the `function` keyword, followed by the function name and a script block.

```powershell
function Greet-User {
    param (
        [string]$Name
    )
    Write-Output "Hello, $Name! Welcome to PowerShell."
}

Greet-User -Name "Diwash"
```
_Output:_
```
Hello, Diwash! Welcome to PowerShell.
```

Functions can accept parameters, return values, and include logic just like in other programming languages. You can also use advanced features like parameter validation and default values.

### Advanced Functions

Advanced functions in PowerShell behave like cmdlets and provide more control over parameters, input processing, and output. You create an advanced function by adding the `[CmdletBinding()]` attribute and using the `param` block.

Example:

```powershell
function Get-Square {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory)]
        [int]$Number
    )
    Write-Output ($Number * $Number)
}

Get-Square -Number 7 # If I don't specify the parameter here, you'll be given a prompt to enter the value. (This is why CmdletBinding() is so awesome.)
```
_Output:_
```
49
```

Advanced functions support features like parameter validation, pipeline input, and help documentation, making your scripts more robust and user-friendly.

## Error Handling with Try/Catch

PowerShell provides structured error handling using `try`, `catch`, and optionally `finally` blocks. This lets you gracefully handle errors and take action when something goes wrong.

Here's a basic example:

```powershell
try {
    # Code that might throw an error
    Get-Content "C:\nonexistentfile.txt"
} catch {
    # Code to run if an error occurs
    Write-Output "Oops! The file does not exist."
}
```

You can also access error details using the `$_` variable inside the `catch` block:

```powershell
try {
    1 / 0
} catch {
    Write-Output "An error occurred: $($_.Exception.Message)"
}
```

The `finally` block (optional) runs whether or not an error occurred—useful for cleanup:

```powershell
try {
    # risky code
} catch {
    # handle error
} finally {
    # always runs
    Write-Output "Done!"
}
```

## Common & Useful Cmdlets for Sysadmins

Here are some of the most frequently used PowerShell cmdlets for system administration and general tasks:

| Cmdlet                | Description                                              |
|-----------------------|---------------------------------------------------------|
| `Get-Process`         | Lists running processes                                 |
| `Stop-Process`        | Stops a running process                                 |
| `Get-Service`         | Lists all services                                      |
| `Start-Service`       | Starts a service                                        |
| `Stop-Service`        | Stops a service                                         |
| `Restart-Service`     | Restarts a service                                      |
| `Get-EventLog`        | Retrieves event logs from local/remote computers        |
| `Get-ChildItem`       | Lists files and directories (like `ls` or `dir`)        |
| `Copy-Item`           | Copies files and folders                                |
| `Move-Item`           | Moves files and folders                                 |
| `Remove-Item`         | Deletes files and folders                               |
| `Set-ExecutionPolicy` | Changes script execution policy                         |
| `Get-Content`         | Reads content from a file                               |
| `Set-Content`         | Writes/replaces content in a file                       |
| `Add-Content`         | Appends content to a file                               |
| `Test-Connection`     | Sends ICMP echo requests (like `ping`)                  |
| `Get-LocalUser`       | Lists local user accounts                               |
| `New-LocalUser`       | Creates a new local user account                        |
| `Get-LocalGroup`      | Lists local groups                                      |
| `Add-LocalGroupMember`| Adds a user to a local group                            |
| `Get-Help`            | Displays help about cmdlets and concepts                |

These cmdlets form the foundation for many administrative scripts and daily tasks.