# -*- coding: utf-8 -*-

from odoo import models, fields, api

class wizard(models.TransientModel):
    _name = 'openacademy.wizard'
    _description = "wizard: Quick Registration of Attendees to Sessions"

    def _default_sessions(self):
        return self.env['openacademy.session'].browse(self._context.get('active_id'))

    session_id = fields.Many2many('openacademy.sessions',
        string="sessions", required=True, default=_default_sessions)
    attendee_ids = fields.Many2many('res.partner'), string="Attendees")

    def subscribe(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
        return{}