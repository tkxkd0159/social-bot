import threading
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import tw

app = FastAPI()
app.state.is_subscribe = False

@app.get("/")
async def root():
    return {"message": "Hello World"}

class TwsubOpts(BaseModel):
    targets: list[str]    # twitter id list(without @)
    tags: list[str]
class TwPatchOpts(TwsubOpts):
    method: str

@app.post("/subscribe")
async def subscribe_twitters(opts: TwsubOpts):

    if not app.state.is_subscribe:
        tw.initialize()
        new_rules = tw.subscribe_targets(opts.targets, opts.tags)
        tw.set_rules(new_rules)
        app.state.twtargets = {"ids": opts.targets, "tags": opts.tags}
        th = threading.Thread(target=tw.get_stream, args=(True, True))
        th.start()
        app.state.is_subscribe = True
        return tw.get_rules()
    return {"result": "Error: exist subscription"}

@app.get("/subscribe")
async def get_subscribe_list():
    return tw.get_rules()

@app.patch("/subscribe")
async def modify_twtargets(opts: TwPatchOpts, response: Response):
    if opts.method == "add":
        app.state.twtargets["ids"].extend(opts.targets)
        app.state.twtargets["tags"].extend(opts.tags)

    elif opts.method == "delete":
        _none = ""
        try:
            for target in opts.targets:
                _none = target
                app.state.twtargets["ids"].remove(target)
            for tag in opts.tags:
                _none = tag
                app.state.twtargets["tags"].remove(tag)

        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"result": f'{_none} not in list'}

    tw.initialize()
    tw.set_rules(tw.subscribe_targets(app.state.twtargets["ids"], app.state.twtargets["tags"]))
    return tw.get_rules()