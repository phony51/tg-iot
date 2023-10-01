from pydantic import BaseModel


class BotSettings(BaseModel):
    token: str


class ControllerSettings(BaseModel):
    ip: str
    port: int


class Config(BaseModel):
    bot: BotSettings
    controller: ControllerSettings


configuration = Config.model_validate_json(open('config.json', 'r').read())
