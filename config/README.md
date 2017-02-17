# Agent Configuration
This directory holds configuration files related to agent specific and logger configurations.


## Liota.conf
liota.conf provides path to find out various configuration & log files.  When initializing, LIOTA does a multi-step search for the configuration file:

* Looks in the current working directory '.'
* User's home directory '~'
* A LIOTA_CONF environment variable
* Finally the default location for every installation: /etc/liota/conf.

#### [LOG_CFG]

* **json_path** holds path to json file that holds logger specific configurations


#### [LOG_PATH]

* **log_path** holds path to log files


#### [UUID_PATH]

* **uuid_path** holds path to file where local_uuid generated and (if) global_uuid obtained from DCCs are stored.


#### [IOTCC_PATH]

* **iotcc_path** holds path to file where IoTCC DCC related entities are stored.


#### [CORE_CFG]

* **collect_thread_pool_size** Size of collection thread pool. Number of threads depends on EdgeSystem's hardware capability and the way (Blocking/Non-blocking) in which metrics are collected from sensors.


#### [CONN_RETRY_CFG]
Configurations specific to Exponential reconnect Back-Off.

* **retry_count -** Number of attempts to re-establish the connection.  **Dafault value is -1**. i.e., Infinite number of attempts.
* **base_backoff_sec -** Time in seconds after which first retry should be attempted. **Default value is 5**.
* **max_backoff_sec -** Maximum exponential back-off time in seconds.  **Dafault value is 3600**
* **min_conn_stability_sec -** Time in seconds after which connection can be marked as stable and **current_reconnect_backoff** time can be reset back to **base_backoff_sec**.


#### [PKG_CFG]
Configurations specific to Package Manager.

* **pkg_path -** Default packages path.
* **pkg_msg_pipe -** Default path for package messenger pipe.
* **pkg_list -** Default path to list of packages to load at start-up.



Feel free to modify ![liota.conf](/config/liota.conf) and ![logging.json](/config/logging.json) as appropriate for your testing.

