using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LumberMill : ObjectInfo
{
    float money;

    public float ExchangeWood(float wood)
    {
        if (wood>0)
        {
            money = wood;    
        }

        return money;
    }
}
