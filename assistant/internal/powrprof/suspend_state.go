package powrprof

import (
	"os"
	"os/exec"
	"path"
)

var WinDir = os.Getenv("windir")
var RunDll = path.Join(WinDir, "System32\\rundll32.exe")

const SetSuspendStatePtr = "powrprof.dll,SetSuspendState"

func SetSuspendState(state string) error {
	c := exec.Command(RunDll, SetSuspendStatePtr, state)
	return c.Run()
}

func Sleep() error {
	return SetSuspendState("0,1,0")
}
