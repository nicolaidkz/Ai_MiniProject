using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FoodShop : ObjectInfo
{
    float food;

    public float ExchangeMoney(float money)
    {
        if (money>0)
        {
            food = money;    
        }

        return food;
    }
}
