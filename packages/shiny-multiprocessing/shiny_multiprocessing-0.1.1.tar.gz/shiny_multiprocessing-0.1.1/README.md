# shiny_multiprocessing

A small token piece of code meant to make multiprocessing a bit handier, when
it comes to executing functions, that need proper monitoring in terms of
idling, timing out or failing with errors.

It makes use of Pebble to reliably enforce timeouts on the individual processes
while also providing comfortable retry capabilities for a range of exceptions
of your selection.

More documentation to come. Maybe.