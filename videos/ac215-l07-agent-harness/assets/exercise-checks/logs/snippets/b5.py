import asyncio
from acts.act3_workflow import build_act3
from formaggio.shop.checkout import Checkout
from formaggio.operations.observability import Recorder
from cli import print_workflow_result


async def main():
    checkout = Checkout()

    async def manager(ticket):
        checkout.store.inventory["mimolette"] -= 2000   # another order ships 2,000 g meanwhile
        return "approve"

    with Recorder("outputs/exercises.sqlite") as recorder:
        result = await build_act3(fixture=True, scenario="manager-approval").run(
            recorder, manager=manager, checkout=checkout)
        print_workflow_result(result)

asyncio.run(main())
