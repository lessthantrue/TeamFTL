[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Drawing") 
[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms") 

$signature=@'
[DllImport("user32.dll",CharSet=CharSet.Auto,CallingConvention=CallingConvention.StdCall)]
public static extern void mouse_event(long dwFlags, long dx, long dy, long cButtons, long dwExtraInfo);
'@

$SendMouseClick = Add-Type -memberDefinition $signature -name "Win32MouseEventNew" -namespace Win32Functions -passThru

DO {
   $x = $Input
   $y = $Input
   echo $x
   echo $y
   $ix = [int]$x
   $iy = [int]$y
   [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point($ix, $iy)
   $SendMouseClick::mouse_event(0x00000002, 0, 0, 0, 0);
   $SendMouseClick::mouse_event(0x00000004, 0, 0, 0, 0);
} WHILE($true)