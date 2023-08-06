# TimerDict

This package provides a simple dictionary-like class, which drops items after a
set amount of time.

```python
from datetime import timedelta
from typing import Union

# When creating a TimerDict specify for how long items should live for:
my_dict = TimerDict(default_duration=timedelta(minutes=5))

# Then add items like you would to any dictionary
my_dict["foo"] = "bar"

# Or use the `put` method if you want to explicitly set the duration for a key
my_dict.put('foo', 'bar', timedelta(seconds=10))

# Getting items also works just like you'd would expect
print(my_dict['foo'])
```

## Implementation Details

Internally, the dict keeps a queue of all items and when they should be removed.
The items are then purged whenever control flow passes to the dictionary, such
as when adding or getting an item. There is no separate thread or `async` task
running in the background.
