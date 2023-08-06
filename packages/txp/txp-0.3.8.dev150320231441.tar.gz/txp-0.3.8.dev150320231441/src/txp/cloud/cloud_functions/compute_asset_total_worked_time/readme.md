### Cloud Function: Compute total worked time

This function will do: 
 
- Download the worked time from machines in the vibrations 
table.
  
- Compute the total worked time _since_ the last checkpoint. 

- Add and UPDATE the value of the new total worked time in the 
`equipments_total_worked_time` table.
  
The function is executed with a Pub/Sub trigger. 
By doing so, we keep the flexibility to invoke the function from 
anywhere and to write business logic if necessary to parametrize 
the function invocation.

**Deploy command**

```commandline
gcloud functions deploy compute_asset_total_worked_time --runtime python37 --trigger-topic total_worked_hours_conveyors
```


