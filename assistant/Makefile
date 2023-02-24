icon.go: icon.ico
	2goarray Icon main < icon.ico > icon.go

.PHONY: build
build: icon.go
	GOOS=windows GOARCH=amd64 go build -ldflags "-H=windowsgui" -o ../dist/pol-assistant.exe
