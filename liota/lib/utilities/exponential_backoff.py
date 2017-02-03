# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------#
#  Copyright © 2015-2016 VMware, Inc. All Rights Reserved.                    #
#                                                                             #
#  Licensed under the BSD 2-Clause License (the “License”); you may not use   #
#  this file except in compliance with the License.                           #
#                                                                             #
#  The BSD 2-Clause License                                                   #
#                                                                             #
#  Redistribution and use in source and binary forms, with or without         #
#  modification, are permitted provided that the following conditions are met:#
#                                                                             #
#  - Redistributions of source code must retain the above copyright notice,   #
#      this list of conditions and the following disclaimer.                  #
#                                                                             #
#  - Redistributions in binary form must reproduce the above copyright        #
#      notice, this list of conditions and the following disclaimer in the    #
#      documentation and/or other materials provided with the distribution.   #
#                                                                             #
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"#
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE  #
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE #
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE  #
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR        #
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF       #
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS   #
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN    #
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)    #
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF     #
#  THE POSSIBILITY OF SUCH DAMAGE.                                            #
# ----------------------------------------------------------------------------#

import random
import logging
import time
import threading

log = logging.getLogger(__name__)


class RandomizedExponentialBackoff:
    """
    This class implements Randomized Exponential BackOff Timer logic for auto-retry in case of network dis-connectivity.

    BackOff Logic: t_cur = min(t_max, random(t_base, 3 * t_curr))

    Option to reset 't_cur' once connection is stable.
    """

    def __init__(self, base_backoff_sec=5, max_backoff_sec=3600, min_conn_stability_sec=10):
        """
        :param base_backoff_sec: Base BackOff Time in seconds.
        :param max_backoff_sec: Maximum BackOff Time in seconds
        :param min_conn_stability_sec: Minimum Connection Stability time in seconds.
        """
        if base_backoff_sec < 0 or max_backoff_sec < 0 or min_conn_stability_sec < 0:
            log.error("Base BackOff, Max BackOff and Min Connection Stability Time must be greater than zero.")
            raise ValueError("Base BackOff, Max BackOff and Min Connection Stability Time must be greater than zero.")

        self._base_backoff_sec = base_backoff_sec
        self._current_backoff_sec = base_backoff_sec
        self._max_backoff_sec = max_backoff_sec
        self._min_conn_stability_sec = min_conn_stability_sec
        # Used to reset t_curr to t_base once connection is stable.
        self._stable_connection_timer = None

    def backoff(self):
        """
        To be invoked in auto-retry logic of Transports.  Returns once `t_cur` is elapsed.
        :return: None
        """
        self.stop_stable_connection_timer()
        log.debug("Current Backoff Time is: {0} sec".format(str(self._current_backoff_sec)))
        # Sleep for t_cur
        time.sleep(self._current_backoff_sec)
        log.debug("After BackOff..")
        # Randomized Exponential BackOff
        # t_cur = min(t_max, random(t_base, 3 * t_curr))
        self._current_backoff_sec = min(self._max_backoff_sec, random.randint(self._base_backoff_sec,
                                                                              3 * self._current_backoff_sec))

    def start_stable_connection_timer(self):
        """
        Starts Connection Stability Timer.
        :return: None
        """
        self._stable_connection_timer = threading.Timer(self._min_conn_stability_sec, self._reset_current_backoff)
        self._stable_connection_timer.start()
        log.debug("Started stable connection timer.")

    def stop_stable_connection_timer(self):
        """
        Stops Connection Stability Timer.
        :return: None
        """
        if self._stable_connection_timer is not None:
            log.debug("Stable connection timer is stopped.")
            self._stable_connection_timer.cancel()
            self._stable_connection_timer = None

    def _reset_current_backoff(self):
        """
        Callback method to be invoked after Connection Stability Time is elapsed.
        :return: None
        """
        log.debug("Connection is stable for : {0} sec.".format(str(self._min_conn_stability_sec)))
        self._current_backoff_sec = self._base_backoff_sec
        self.stop_stable_connection_timer()
