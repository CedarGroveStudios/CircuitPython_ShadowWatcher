# SPDX-FileCopyrightText: Copyright (c) 2022 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: Unlicense

import time
import board
from cedargrove_shadowwatcher import ShadowWatcher

# Instantiate shadow detector class and establish background level
gesture = ShadowWatcher(pin=board.LIGHT, auto=True)

while True:
    if gesture.detect():
        print("SHADOW DETECTED")
        while gesture.detect():
            # Wait until the shadow is gone
            time.sleep(1)
        # Rebaseline the background level
        gesture.refresh_background()
        print(f"background: {gesture.background:6.0f}")
