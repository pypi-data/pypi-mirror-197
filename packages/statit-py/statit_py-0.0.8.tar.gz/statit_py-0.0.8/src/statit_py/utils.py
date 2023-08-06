from typing import Callable

def table_to_obs(table: list[list], line_to_date: Callable[[list], str | None], line_to_value: Callable[[list], int | float | None], line_to_key: Callable[[list], str | None]) -> dict[str, list[tuple[str, int | float | None]]]:
     """
     Takes a table (csv file) and outputs a dictionary of observations

     Arguments
     ----------
          table : list(list)
               A list of lines (an line is line in a CSV file)
          line_to_date : (list) -> str | None
               A function whose input is a line and output is the corresponding date, if there exists one
          line_to_value : (list) -> int | float | None
               A function whose input is a line and output is the corresponding value, if there exists one
          line_to_key : (list) -> str | None
               A function whose input is a line and output is the corresponding key of the serie, if there exists one
     
     Out
     ---
     A dictionary whose values are a list of observations

     """
     #create observation lists, mapped by id
     CHARS = '#####'
     key_datified = {
        line_to_key(line)+CHARS+line_to_date(line)+CHARS+str(i) : line_to_value(line)
        for line,i in zip(table,range(len(table)))
        if line_to_date(line) and line_to_key(line)
     }
     aggregated = {}
     for key, value in key_datified.items():
            k=(key.split(CHARS)); k=k[0]+CHARS+k[1]
            try:
                aggregated[k] += value
            except(KeyError):
               aggregated[k] = (value if (value!=None and value!='') else 0)
            except(TypeError):
                pass

     observations = {}
     for key,value in aggregated.items():
          k = key.split(CHARS)
          try:
               observations[k[0]].append((k[1], value))
          except(KeyError):
               observations[k[0]] = [(k[1], value)]
     
     return observations

