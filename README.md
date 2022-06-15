# printerwatch_server_edition
a reworked version of printerwatch that runs on a ubuntu/apache2 server with a webinterface

lets take a quick look at how it is used, 

![Login](https://user-images.githubusercontent.com/16318230/173759082-2d112c9f-071a-440b-bff6-fadb31e2be1a.png)

be aware the information on the login-screen-picture where used by me during the development, 
and i included them on the image since i also used it for some user that i had testing the webinterface.

![PrinterMonitor](https://user-images.githubusercontent.com/16318230/173759096-3d850bb4-2464-4da7-be14-69dfa2b4727b.png)

Not included on the image but there is more information you can get out of this page the logo on the top left corner will show the time of
the last time the data got updated ( also the yellow bits get grayed out if it was more then an hour ago ) but it only updates up on entering the site.
Hovering over the cartridge fill values will show a tooltip with the cartridge types.

![CartridgeStorage](https://user-images.githubusercontent.com/16318230/173759117-531ba79c-eb21-4903-9d13-75881f18925a.png)

the math is correct but useualy printer usage shows some fluctuation, and the estimation only uses the average value that said more data most likely will
lead to more accurate estaminations but some offset is to be expected.
Another thing to mention is the evaluation when a cartridge is replaced is simple it will trigger as soon a cartridge shows a higher percentage then on the
previous messurement. That means things like reseting or switching around ( maybe to check if some issue was produced by them ) toner can lead to 
falsely triggering the counter.

![Analytics](https://user-images.githubusercontent.com/16318230/173759136-078f399b-ed9e-4dc7-bd16-1ee0e31eb334.png)

![DeviceManager](https://user-images.githubusercontent.com/16318230/173759203-965ade1b-ecdf-47ff-a977-03a45f75bc5e.png)
