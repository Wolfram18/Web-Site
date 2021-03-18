from background_task import background


@background(schedule=5)
def background_process(s1: str, s2: str) -> None:
   """
   Does something that takes a long time
   :param p1: first parameter
   :param p2: second parameter
   :return: None
   """
   pass