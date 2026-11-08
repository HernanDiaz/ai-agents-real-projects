Notes from a conversation with Danny (web) and Martha (management), on October 23.

- Danny: "If a size is sold out and we don't give them an option, the customer buys
  from another store."
- Only bikes can be backordered (references starting with UR, MT, CR, EL or IN, like
  `BIKE_PREFIXES` in config.py). Accessories can't: they are restocked right away and
  it's not worth it.
- A backorder only makes sense if the size is sold out. If there are units, they should
  buy it.
- Martha: "If the supplier hasn't given us a restock date, no backorder: we can't keep
  people waiting without knowing until when."
- Martha: "And if the date isn't confirmed, don't show it. They can backorder, but
  without promising a date: we'll let them know." Unconfirmed dates nearly always
  change.
- (Danny asked whether we could charge a deposit. Martha: not for now.)
