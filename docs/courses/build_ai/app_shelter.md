# 🐕 Shelter Desk

```csv
name,breed,age,fee
Biscuit,Beagle,3,120
Scout,Collie,5,90
Nova,Husky,2,
```
{: .dataset #dogs }

[The dogs](#)
{: .datagrid source="dogs" #dog_list editable="true" height="190" title="Waiting for a home" }

[Adoption fees](#)
{: .chart source="dogs" #fee_chart type="bar" x="name" y="fee" height="200" title="Adoption fee (€)" }
