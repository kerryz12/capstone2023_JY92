if (TARGET tinyusb_device)
        add_executable(heartrate
                heartrate.c
                )

# pull in common dependencies
target_link_libraries(heartrate 
        pico_stdlib
        pico_cyw43_arch_none)

 # enable usb output, disable uart output
 pico_enable_stdio_usb(heartrate 1)
 pico_enable_stdio_uart(heartrate 0)

# create map/bin/hex file etc.
pico_add_extra_outputs(heartrate)

# add url via pico_set_program_url
example_auto_set_url(heartrate)

elseif(PICO_ON_DEVICE)
    message(WARNING "not building hello_usb because TinyUSB submodule is not initialized in the SDK")
endif()



