from datetime import datetime
from loguru import logger

from yum_hal.ticket import Ticket


def test_codec():
    t = Ticket(code="1001")
    t.put("a", 1)
    t.put("b", datetime.now())
    t.put("c", None)
    t.put("d", False)
    o = t.encode()
    logger.info("encoded: {}", o)

    t1 = Ticket(code="")
    t1.decode(o)
    logger.info("t1 datetime: {}", t1.take("b"))
    assert t1.take("b") == t.take("b")
