#!/bin/bash
# https://github.com/pzmarzly/mic_over_mumble
set -euo pipefail
# To debug, uncomment the following line:
# set -x

# PAID = PulseAudio ID
# ID = PID / process ID

main () {
    set_up
    echo "Press Return to restore PulseAudio configuration..."
    read -n1 -s -r
}


set_up () {
    change_pa_config
    echo "Done. Please use pavucontrol to ensure everything works."
    print_ip
}

shut_down () {
    echo "Shutting down..."
    restore_pa_config
}

change_pa_config () {
    echo "Changing PulseAudio configuration..."
    add_sink
    move_discord_to_sink
    add_source
    set_default_source
}

restore_pa_config () {
    echo "Restoring PulseAudio configuration..."
    remove_source
    remove_sink
}

# PA utilities.

add_sink () {
    echo "Adding sink..."
    SINK_MODULE_PAID=$(pactl load-module \
        module-null-sink \
        sink_name=Loopback_of_Discord \
        sink_properties=device.description=Loopback_of_Discord)
    echo $SINK_MODULE_PAID
    sleep 1
    SINK_PAID=$(get_sink_paid)
}

remove_sink () {
    pactl unload-module "$SINK_MODULE_PAID"
}

add_source () {
    echo "Adding a virtual microphone..."
    SOURCE_MODULE_PAID=$(pactl load-module module-virtual-source source_name=VirtualMicDiscord \
        master=Loopback_of_Discord.monitor source_properties=device.description=VirtualMicDiscord)
}

remove_source () {
    pactl unload-module "$SOURCE_MODULE_PAID"
}

move_discord_to_sink () {
    echo "Move discord to sink..."
    DISCORD_CLIENT_PAID=$(get_discord_client_paid)
    pacmd move-sink-input "$DISCORD_CLIENT_PAID" "$SINK_PAID"
}

set_default_source () {
    pactl set-default-source VirtualMicDiscord
}
# Data fetching & parsing.

get_discord_client_paid () {
    result=$(pacmd list-sink-inputs |
        grep -F -e "index: " -e "media.name = " |
        cut_every_second_newline |
        grep -F -e "playStream" |
        take_second_column)

    if [ -z "$result" ]; then
        echo "Error: Discord client did not connect to PulseAudio (yet?)." 2>&1
        print_how_to_restart 2>&1
        exit 1
    fi

    if [ "$(echo "$result" | wc -l)" != "1" ]; then
        echo "Error: Multiple Discord instances found." 2>&1
        print_how_to_restart 2>&1
        exit 1
    fi

    echo "$result"
}

get_sink_paid () {
    result=$(pacmd list-sinks |
        grep -F -e "index: " -e "name: " |
        cut_every_second_newline |
        grep -F -e "Loopback_of_Discord" |
        cut_active_device_indicator |
        take_second_column | head -n 1)

     if [ -z "$result" ]; then
        echo "Error: Failed to find the device the script should have added." 2>&1
        print_how_to_restart 2>&1
        exit 1
    fi

    if [ "$(echo "$result" | wc -l)" != "1" ]; then
        echo "Error: Multiple virtual devices found." 2>&1
        print_how_to_restart 2>&1
        exit 1
    fi

    echo "$result"
}

# https://serverfault.com/a/375098/449626
cut_every_second_newline () {
    awk 'ORS=NR%2?" ":"\n"'
}

take_second_column () {
    awk '{print $2}'
}

# See https://github.com/pzmarzly/mic_over_mumble/issues/5 .
# The initial whitespace may contain an asterisk if the current
# device is the default one.
cut_active_device_indicator () {
    cut -c 5-
}

print_ip () {
    if ! [ -x "$(command -v ip)" ]; then
        echo "Skipping IP printing: ip command not found..."
        return
    fi
    if ! [ -x "$(command -v jq)" ]; then
        echo "Skipping IP printing: jq command not found..."
        return
    fi
    echo "Your IP addresses:"
    set +e
    ip -j addr | jq -r ".[] | .addr_info | .[] | select(.family==\"inet\") | select(.local != \"127.0.0.1\") | .local"
    set -e
}

# Errors

print_how_to_restart () {
    echo "Please find the reason why this happened, try fixing it"
    echo "(\`pacmd list-sink-inputs\` and \`pacmd list-sinks\` may be"
    echo "useful), then kill discord, restart PulseAudio via"
    echo "\`pulseaudio -k\`, and finally, restart the script."
}

main