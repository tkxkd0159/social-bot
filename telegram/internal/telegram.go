package internal

import (
	"fmt"
	"log"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

type TeleSendForm struct {
	ChatID int64
	Msg    string
}

func SendMultiMsg(b *tgbotapi.BotAPI, sf []TeleSendForm) {
	defer func() {
		if e := recover(); e != nil {
			log.Println(e)
		}
	}()
	for i := 0; i < len(sf); i++ {
		tgtMsg := tgbotapi.NewMessage(sf[i].ChatID, sf[i].Msg)

		if _, err := b.Send(tgtMsg); err != nil {
			panic(fmt.Sprintf("Unexpected error during send msg : %v", err))
		}
	}
}
