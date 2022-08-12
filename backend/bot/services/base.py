from database import get_session_no_gen

class BaseService():

    # mostly 'cause tests I added opportunity to set session, maybe it can be useful anyway, but in real app I'm preferred testing with mocks
    def create_or_set_session(self, session=None):
        if session:
            self.session = session
            return
        self.session = get_session_no_gen()

    async def close_session(self):
        await self.session.close()
