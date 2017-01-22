#!/usr/bin/env python
#coding: utf-8

import main
import json

offerId = 2
accessToken = "EAAHgEYXO0BABABt1QAdnb4kDVpgDv0RcA873EqcNbHFeN8IZANMyXZAU736VKOj1JjSdOPk2WuZC7KwJZBBD76CUbA09tyWETQpOd5OCRSctIo6fuj7cMthZCH6pZA6PZAFmrMgGZChehXreDa3caIZBkBwkyakDAGA4exqgy2sI7JwZDZD"
advertise_groups=["23842535257740719","23842531499950719"]
time_ranges=["2017-01-17","2017-01-18"]
db = main.models.Advertisers
result = db.query.filter_by(offer_id=offerId).first()
print result.id
# date_data_detail(offerId,accessToken,advertise_groups,time_ranges)
