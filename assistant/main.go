package main

import (
	"io"
	"log"
	"net/http"
	"power-assistant/internal/powrprof"
	"time"

	"github.com/getlantern/systray"
)

const Port = "1312"

func handleSleep(w http.ResponseWriter, r *http.Request) {
	log.Printf("Got sleep request from %v", r.RemoteAddr)
	if r.Method != "POST" {
		return
	}
	io.WriteString(w, "ok\n")
	go func() {
		time.Sleep(500 * time.Millisecond)
		powrprof.Sleep()
	}()
}

func main() {
	http.HandleFunc("/pol/sleep", handleSleep)
	log.Printf("PoL assistant is starting on 0.0.0.0:%v ", Port)
	go http.ListenAndServe(":"+Port, nil)
	systray.Run(onReady, onExit)
}

func onExit() {
	log.Println("Exit")
}

func onReady() {
	systray.SetTemplateIcon(Icon, Icon)
	systray.SetTitle("PoL Assistant")
	systray.SetTooltip("PoL Assistant")

	mStatus := systray.AddMenuItem("Status: Running on 0.0.0.0:"+Port, "")
	mStatus.Disable()

	mQuit := systray.AddMenuItem("Quit", "Quit the whole app")
	go func() {
		<-mQuit.ClickedCh
		systray.Quit()
	}()
}
