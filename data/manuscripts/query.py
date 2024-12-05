# type of states:
COPY_EDIT = 'CED'
IN_REF_REV = 'REV'
REJECTED = 'REJ'
SUBMITTED = 'SUB'
TEST_STATE = SUBMITTED
VALID_STATES = [
    COPY_EDIT,
    IN_REF_REV,
    REJECTED,
    SUBMITTED,
]
def get_states() -> list:
    return VALID_STATES
def is_valid_state(state: str) -> bool:
    return state in VALID_STATES


# type of actions:
ACCEPT = 'ACC'
ASSIGN_REF = 'ARF'
DONE = 'DON'
REJECT = 'REJ'


# testing purposes:
TEST_ACTION = ACCEPT
VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DONE,
    REJECT,
]


def get_actions() -> list:
    return VALID_ACTIONS


def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS

FUNC = 'f'

STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            FUNC: lambda x: IN_REF_REV,
        },
        REJECT: {
            FUNC: lambda x: REJECTED,
        },
    }
}
def handle_action(curr_state, action) -> str:
   if curr_state not in STATE_TABLE:
       raise ValueError(f'Bad state: {curr_state}')
   if action not in STATE_TABLE[curr_state]:
       raise ValueError(f'{action} not available in {curr_state}')
   return STATE_TABLE[curr_state][action][FUNC](1)


def main():
    print(handle_action(SUBMITTED, ASSIGN_REF))
    print(handle_action(SUBMITTED, REJECT))