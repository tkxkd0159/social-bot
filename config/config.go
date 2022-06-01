package config

import (
	"fmt"
	"github.com/spf13/viper"
)

func Set() {
	viper.SetConfigFile(".env")
	err := viper.ReadInConfig() // Find and read the config file
	if err != nil {
		panic(fmt.Errorf("Fatal error config file: %w \n", err))
	}
}
