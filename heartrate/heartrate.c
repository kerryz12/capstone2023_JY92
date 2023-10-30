/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

//SDA - 26 GP20
//SCL - 27 GP21

/*
#include "pico/stdlib.h"
#include <stdio.h>

#define SDA_PIN 26
#define SCL_PIN 27

int main() {
#ifndef PICO_DEFAULT_LED_PIN
#warning blink example requires a board with a regular LED
#else
    const uint LED_PIN = PICO_DEFAULT_LED_PIN;
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    while (true) {
        gpio_put(LED_PIN, 1);
        sleep_ms(250);
        gpio_put(LED_PIN, 0);
        sleep_ms(250);
    }
#endif
}
*/

#include "hardware/gpio.h"
#include "pico/stdlib.h"
#include <stdio.h>
#include <math.h>
#include "pico/cyw43_arch.h"

#define SDA_PIN 26
#define SCL_PIN 27

typedef struct {
    float heart_rate;
} hr_reading;

int main() {
    stdio_init_all();
    if (cyw43_arch_init()) {
        printf("Wi-Fi init failed");
        return -1;
    }
    while (true) {
        cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1);
        sleep_ms(250);
        cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 0);
        sleep_ms(250);
        printf("Hello world!");
    }

}


