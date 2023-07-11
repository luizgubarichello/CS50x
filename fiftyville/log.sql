-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Getting the crime scene report description of the stolen duck
SELECT * FROM crime_scene_reports WHERE description LIKE '%duck%';
-- It happened at Humphrey Street on 2021/07/28 10:15AM

-- Getting the interviews of the witnesses
SELECT * FROM interviews WHERE transcript LIKE '%bakery%';
-- Ruth, Eugene and Raymond were witnesses
-- Ruth said the thief escaped by car
-- Emma recognized the thief because she saw him earlier withdrawing money at the ATM on Leggett Street
-- Raymond saw the thief talking on the phone with the accomplice as he left the bakery; they were telling them to buy a flight ticket out of town ASAP for the other morning

-- Getting the security logs from the camera because of what Ruth said
SELECT * FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = 'exit';
-- Above is possible to get all the license plates that left the parking lot within the time frame described by Ruth

-- Getting atm reports because of Emma
SELECT * FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';
-- I should get the bank accounts of this people
SELECT * FROM bank_accounts WHERE account_number in
(SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
);
-- Now i'm able to get the names of these people
SELECT * FROM people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number in
(SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
));
-- Now i can check whose car left the bakery parking lot
SELECT * FROM people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number in
(SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
)) AND license_plate IN
(SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = 'exit'
);
-- With this I can assume the thief is one of the people from the table above

-- Getting phone calls data from what Raymond said
SELECT * FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;
-- Checking if any of the people gotten from the license_plate is a caller
SELECT * FROM people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number in
(SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
)) AND license_plate IN
(SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = 'exit'
) AND phone_number IN
(SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60
);
-- Now i have less people to worry about
-- I will get the flights of these people
SELECT flight_id FROM passengers WHERE passport_number in
(SELECT passport_number FROM people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number in
(SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
)) AND license_plate IN
(SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = 'exit'
) AND phone_number IN
(SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60
));
-- I will now get the flights made on the other morning
SELECT flight_id FROM flights WHERE day = 29 AND hour < 12 AND id in
(SELECT flight_id FROM passengers WHERE passport_number in
(SELECT passport_number FROM people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number in
(SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
)) AND license_plate IN
(SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = 'exit'
) AND phone_number IN
(SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60
)));
-- Now i know the flight, i just need to get the person name
SELECT * FROM people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number in
(SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
)) AND license_plate IN
(SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = 'exit'
) AND phone_number IN
(SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60
) AND passport_number IN
(SELECT passport_number FROM passengers WHERE flight_id = 36 AND passport_number in
(SELECT passport_number FROM people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number in
(SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
)) AND license_plate IN
(SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = 'exit'
) AND phone_number IN
(SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60
)));
-- It's Bruce!
-- Now i get who he called
SELECT * FROM people WHERE phone_number IN
(SELECT receiver FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60 and CALLER = '(367) 555-5533'
);
-- It's Robin!
-- Now i only need to get where Bruce escaped to
SELECT * FROM airports WHERE id = 4;
-- New York City!