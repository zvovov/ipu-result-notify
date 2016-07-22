# IPU Result Notify
Get email notifications when IP University uploads exam results.

## What is this
This python script monitors the [IP University results page](http://www.ipu.ac.in/exam_results.php) for any changes. An email is sent to the user whenever there is a change.

## Why
To save the F5 key from incessant torture.


## How To
1. Clone this repository.
    ```
    $ git clone https://github.com/zvovov/ipu-result-notify.git
    ```

2. Install the requirements.
    ```
    $ pip install -r requirements.txt
    ```

3. Enter sender's email (gmail), password and receiver's email(s) (any) in ```results.py```.
    ```
    from_addr = "SENDER_EMAIL"
    to_addr = ["RECEIVER_EMAIL", "RECEIVER_EMAIL"]
    ...
    server.login(from_addr, "PASSWORD")
    ```
    You can even enter the same email (gmail) in sender and receiver to send emails to yourself.

4. Run the script.
    Only runs on Python 3.x
    ```
    $ python result.py 600
    ```
    ```600``` is the time interval (in seconds) after which the script will check if the result page has changed. This wait-check process will go on, unless stopped using ```Ctrl-C```.

5. Run this script on your machine or on a server.

    ![Email from IPU Result Notify](http://i.imgur.com/VVx48V4.jpg "Email from IPU Result Notify")

6. Profit.

##License
[MIT](https://github.com/zvovov/ipu-result-notify/blob/master/LICENSE)
