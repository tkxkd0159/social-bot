package main

import (
	"fmt"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/spf13/viper"
	"log"
	"strconv"
	"time"
)
import (
	"github.com/tkxkd0159/go-telebot/config"
	"github.com/tkxkd0159/go-telebot/internal"
)

func main() {
	config.Set()
	bot, err := tgbotapi.NewBotAPI(viper.Get("TELEGRAM_APITOKEN").(string))
	if err != nil {
		panic(err)
	}

	//bot.Debug = true
	updateConfig := tgbotapi.NewUpdate(0)
	updateConfig.Timeout = 30

	// Start polling Telegram for updates.
	updates := bot.GetUpdatesChan(updateConfig)
	startTime := time.Now()

	// Each update that get from Telegram
	// channel로 Telegram으로부터의 데이터 수신 대기
	go func() {
		for update := range updates {
			if update.Message == nil {
				continue
			}
			msg := tgbotapi.NewMessage(update.Message.Chat.ID, update.Message.Text)
			msg.ReplyToMessageID = update.Message.MessageID

			if m, err := bot.Send(msg); err != nil {
				panic(err)
			} else {
				fmt.Println("From gotele bot : \n", m.Text)
			}
		}
	}()
	cid, err := strconv.ParseInt(viper.GetString("TELEGRAM_BOT_CHAT_ID"), 10, 64)
	if err != nil {
		log.Fatalf("You need to set chat-id to send \n")
	}

	for {
		time.Sleep(time.Second * 5)
		pollLog := fmt.Sprintf("This polling machine has been running for %s \n", time.Now().Sub(startTime))
		fmt.Println(pollLog)

		first := internal.TeleSendForm{ChatID: cid, Msg: pollLog}
		second := internal.TeleSendForm{ChatID: cid, Msg: "I am second msg"}
		msgList := []internal.TeleSendForm{first, second}
		internal.SendMultiMsg(bot, msgList)
	}
}
