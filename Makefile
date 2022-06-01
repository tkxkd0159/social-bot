TARGET ?= bot


.PHONY: build clean run

run :
	@echo "###### Run bot ######\n"
	@go run ./cmd/$(TARGET)

build :
	go build -o bin/$(TARGET) ./cmd/$(TARGET)

clean :
	rm -rf ./bin/