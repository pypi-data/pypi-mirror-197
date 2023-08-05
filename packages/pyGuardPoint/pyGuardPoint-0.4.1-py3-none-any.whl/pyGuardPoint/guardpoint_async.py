from asyncio import Future
from concurrent.futures import ThreadPoolExecutor
from .guardpoint import GuardPoint, GuardPointError


class GuardPointAsync:

    def __init__(self, **kwargs):
        self.gp = GuardPoint(**kwargs)
        self.executor = ThreadPoolExecutor(max_workers=1)

    def get_card_holder(self, on_finished, uid=None, card_code=None):
        future = self.executor.submit(self.gp.get_card_holder, uid=uid, card_code=card_code)
        callback = GPAsyncCallBack(on_finished)
        future.add_done_callback(callback.handle_future)

    def get_card_holders(self, on_finished, offset=0, limit=10, search_terms=None, cardholder_type_name=None, areas=None,
                         filter_expired=False):
        future = self.executor.submit(self.gp.get_card_holders, offset=offset, limit=limit, search_terms=search_terms,
                                      cardholder_type_name=cardholder_type_name, areas=areas, filter_expired=filter_expired)
        callback = GPAsyncCallBack(on_finished)
        future.add_done_callback(callback.handle_future)

    def get_cards(self, on_finished):
        future = self.executor.submit(self.gp.get_cards)
        callback = GPAsyncCallBack(on_finished)
        future.add_done_callback(callback.handle_future)

    def delete_card(self, on_finished, card):
        future = self.executor.submit(self.gp.delete_card)
        callback = GPAsyncCallBack(on_finished)
        future.add_done_callback(callback.handle_future, card)

    def get_areas(self, on_finished):
        future = self.executor.submit(self.gp.get_areas)
        callback = GPAsyncCallBack(on_finished)
        future.add_done_callback(callback.handle_future)


class GPAsyncCallBack:
    on_finished = None

    def __init__(self, on_finished_func):
        self.on_finished = on_finished_func

    def handle_future(self, future):
        try:
            r = future.result()
            self.on_finished(r)
        except GuardPointError as e:
            self.on_finished(e)
        except Exception as e:
            self.on_finished(GuardPointError(e))
