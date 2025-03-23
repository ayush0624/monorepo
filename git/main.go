package main

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

func main() {
	var rootCmd = &cobra.Command{
		Use:   "binary",
		Short: "A simple CLI application",
		Long:  `A simple CLI application built with Cobra and Bazel.`,
		Run: func(cmd *cobra.Command, args []string) {
			fmt.Println("Hello from the Cobra CLI!")
		},
	}

	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
} 