add_executable(heartrate
        heartrate.c
        )

# pull in common dependencies
target_link_libraries(heartrate pico_stdlib)

# create map/bin/hex file etc.
pico_add_extra_outputs(heartrate)

# add url via pico_set_program_url
example_auto_set_url(heartrate)
