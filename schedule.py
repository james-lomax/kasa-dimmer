import asyncio
from bulb import find_device
from datetime import datetime, timedelta


DEVICE_NAME = "bedroom"
COLOR_HUE = 20

START_TIME = "07:00"
START_SATURATION = 100
START_BRIGHTNESS = 0
END_SATURATION = 0
END_BRIGHTNESS = 100
DURATION_SECONDS = 60*30


async def wait_until(time_of_day: str):
    # Parse the target time from the input string.
    target_time = datetime.strptime(time_of_day, "%H:%M").time()

    # Get the current time.
    now = datetime.now()

    # Construct a datetime object for the target time today.
    target_datetime = datetime.combine(now.date(), target_time)

    # If the target time is in the past, add a day to the target datetime.
    if target_datetime < now:
        target_datetime += timedelta(days=1)

    # Calculate the number of seconds to wait.
    wait_seconds = (target_datetime - now).total_seconds()

    # Wait for the target time.
    print(f"Waiting until {time_of_day} ({wait_seconds} seconds)")
    await asyncio.sleep(wait_seconds)


async def run():
    await wait_until(START_TIME)

    bulb = await find_device(DEVICE_NAME)
    assert bulb is not None

    # Calculate the step size for saturation and brightness interpolation.
    saturation_step = (END_SATURATION - START_SATURATION) / DURATION_SECONDS
    brightness_step = (END_BRIGHTNESS - START_BRIGHTNESS) / DURATION_SECONDS

    # Initialize the current saturation and brightness values.
    current_saturation = START_SATURATION
    current_brightness = START_BRIGHTNESS

    # Iterate for the specified duration.
    for _ in range(DURATION_SECONDS):
        # Update the bulb with the current saturation and brightness values.
        print("Updating bulb: ", current_saturation, current_brightness)
        await bulb.set_hsv(COLOR_HUE, int(current_saturation), int(current_brightness))

        # Increment the current saturation and brightness values.
        current_saturation += saturation_step
        current_brightness += brightness_step

        # Wait for one second.
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(run())
