
select t.in_reply_to_screen_name as referredToName,
from twitter_miner_laptop.tweets t
where t.in_reply_to_screen_name is not null;



SELECT
    u.userID AS toId,
    r.referring AS fromId,
    u.screen_name,
    r.tid
FROM
    twitter_miner_laptop.users u
        INNER JOIN
    (SELECT
    t.tweetID as tid,
        t.in_reply_to_screen_name AS sn,
        t.userID AS referring
    FROM
        twitter_miner_laptop.tweets t
    WHERE
        t.in_reply_to_screen_name IS NOT NULL) AS r
WHERE
    u.screen_name = r.sn;