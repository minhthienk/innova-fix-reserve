#include <FileConstants.au3>
#include <MsgBoxConstants.au3>
#include <WinAPIFiles.au3>
#include <GuiToolbar.au3>
#include <Array.au3>
;$aArray = _WinGetControls('OBD Capture Tool 3.0.42')
;$comPort = 'COM6'
;$capPath = 'CaptureTool 3.0.42\CaptureTool.exe'




$cmdArr = ReadCmd()

If $cmdArr[1] = 'RUN' Then
   $capPath = $cmdArr[2]
   $comPort = $cmdArr[3]
   RunCaptureTool($capPath, $comPort)

ElseIf $cmdArr[1] = 'LOAD' Then
   $capHandle = $cmdArr[2]
   $simPath = $cmdArr[3]
   LoadSim($capHandle, $simPath)

ElseIf $cmdArr[1] = 'IS_DATA_EXISTING' Then
   $capHandle = $cmdArr[2]
   IsDataExisting($capHandle)

ElseIf $cmdArr[1] = 'CLEAR_DATA' Then
   $capHandle = $cmdArr[2]
   ClearData($capHandle)
EndIf






Func ClearData($capHandle)
   $capHandle = HWnd(String($capHandle))

   Local $clearButton = 'WindowsForms10.BUTTON.app.0.141b42a_r9_ad110'

   ControlClick($capHandle, '', $clearButton)
   WriteLog('done')
EndFunc




Func IsDataExisting($capHandle)
   $capHandle = HWnd(String($capHandle))

   Local $dataTextControl = 'WindowsForms10.EDIT.app.0.141b42a_r9_ad14'

   Local $text = ControlGetText($capHandle, '', $dataTextControl)
   If ($text<>'') Then
	  WriteLog('true')
   Else
      WriteLog('false')
   EndIf
EndFunc








Func RunCaptureTool($capPath, $comPort)
   Local $pid = Run($capPath)
   If @error<>0 Then
	  WriteLog('run failed')
	  Return
   EndIf

   Local $capHandle = WinHandFromPID($pid, "", 3)
   ControlSetText($capHandle, '', 'Edit1', $comPort)

   Local $connectButton = 'WindowsForms10.BUTTON.app.0.141b42a_r9_ad11'
   ControlClick($capHandle, '', $connectButton)

   Local $simName = 'capinit.sim'
   LoadSim($capHandle, $simName)
   WriteLog('run successful: ' & String($capHandle))
EndFunc




Func LoadSim($capHandle, $simName)
   $capHandle = HWnd(String($capHandle))

   If ($simName='') Then
      $simName='noname'
   EndIf

   Local $loadButton = 'WindowsForms10.BUTTON.app.0.141b42a_r9_ad14'
   Local $startButton = 'WindowsForms10.BUTTON.app.0.141b42a_r9_ad15'

   ; get load sim handle
   ControlClick($capHandle, '', $loadButton) ; not lose focus
   $title = 'Save Simulation DataBase'
   $handle = WinWait($title)
   Sleep(1000) ; wait for the dialog to appear

   ; if this is the first sim loading => set the inial folder
   If $simName='capinit.sim' Then
	  ControlCommand($handle, "", "ToolbarWindow324", "SendCommandID", '202')
	  Send(@ScriptDir & '\sim')
	  Send('{ENTER}')
   EndIf


   ; fill simulate file name
   ControlSetText($handle, '', 'Edit1', $simName)
   Sleep(500)

   ControlClick($handle, '', 'Button1')
   Sleep(500)



   ; check if the file name is correct
   $res = ControlSetText($handle, '', 'DirectUIHWND1', '')
   If ($res) Then
      WriteLog('capture load failed')
      While (True)
         $handle = WinGetHandle ($title)
         $ret = WinClose($handle)
         If ($ret=0) Then
            ExitLoop
         EndIf
      WEnd
   Else
      While (True)
         $txt = ControlGetText($capHandle, '', $startButton)
         Sleep(1000)
         If ($txt='stop [ESC]') Then
            ExitLoop
         Else
            Sleep(200)
         EndIf
      WEnd

	  While (WinClose('Notes'))
		 Sleep(100)
	  WEnd

      WriteLog('capture load successful')
   EndIf
EndFunc





Func FocusCurrentActive($wcurr, $timeout)
   Local $currentTitle = WinGetTitle($wcurr)
   Local $count = 0
   While (True)
	  Local $lastTitle = WinGetTitle("[ACTIVE]")
	  If $lastTitle<>$currentTitle Then
		 WinActivate($wcurr)
		 ConsoleWrite('Get Focus Successfully' & @CRLF)

		 ExitLoop

	  EndIf

	  $count = $count + 1
	  If $count=$timeout Then
		 ConsoleWrite('Time out' & @CRLF)
		 ExitLoop
	  EndIf

	  Sleep(1)
   WEnd
EndFunc









Func ReadCmd()
   ; Open the file for reading and store the handle to a variable.
   Local $hFileOpen = FileOpen('temp', $FO_READ)
   ; Read the contents of the file using the handle returned by FileOpen.
   Local $sInfo = FileRead($hFileOpen)
   $arr = StringSplit($sInfo, @CRLF, $STR_ENTIRESPLIT)
   ; Close the handle returned by FileOpen.
   FileClose($hFileOpen)
	Return $arr
EndFunc









Func WriteLog($txt)
   ; Open the file for writing (append to the end of a file) and store the handle to a variable.
   Local $filePath = 'temp'
   Local $hFileOpen = FileOpen($filePath, $FO_OVERWRITE)

   ; Write data to the file using the handle returned by FileOpen.
   FileWrite($hFileOpen, $txt)

   ; Close the handle returned by FileOpen.
   FileClose($hFileOpen)
EndFunc



Func WinHandFromPID($pid, $winTitle="", $timeout=1)
   Local $secs = 0
   Do
      $wins = WinList($winTitle)
      For $i = 1 To UBound($wins)-1
         If (WinGetProcess($wins[$i][1]) == $pid) And (BitAND(WinGetState($wins[$i][1]), 2)) Then Return $wins[$i][1]
      Next
      Sleep(1000)
      $secs += 1
   Until $secs == $timeout
EndFunc

















#include "Array.au3"
Opt("WinTitleMatchMode", 4)
Func _WinGetControls($Title, $Text="")
   Local $WndControls, $aControls, $sLast="", $n=1
   $WndControls = WinGetClassList($Title, $Text)
   $aControls = StringSplit($WndControls, @CRLF)
   Dim $aResult[$aControls[0]+1][2]
   For $i = 1 To $aControls[0]
      If $aControls[$i] <> "" Then
         If $sLast = $aControls[$i] Then
            $n+=1
         Else
            $n=1
         EndIf
         $aControls[$i] &= $n
         $sLast = StringTrimRight($aControls[$i],1)
      EndIf
      If $i < $aControls[0] Then
         $aResult[$i][0] = $aControls[$i]
         ConsoleWrite($aControls[$i] & @CRLF)
      Else ; last item in array
         $aResult[$i][0] = WinGetTitle($Title) ; return WinTitle

      EndIf
      $aResult[$i][1] = ControlGetHandle($Title, $Text, $aControls[$i])
   Next
   $aResult[0][0] = "ClassnameNN"
   $aResult[0][1] = "Handle"
   Return $aResult
EndFunc




