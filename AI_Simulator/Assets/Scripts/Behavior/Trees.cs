using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Trees : ObjectInfo
{
    float amountRemaining = 1;

    public float Chop(float amount, float chopSpeed)
    {
        float amountChopped = Mathf.Max(0, Mathf.Min(amountRemaining, amount));
        amountRemaining -= amount * chopSpeed;

        transform.localScale = Vector3.one * amountRemaining;

        if (amountRemaining <= 0)
        {
            Die(CauseOfDeath.Eaten);
        }

        return amountChopped;
    }

    public float AmountRemaining
    {
        get
        {
            return amountRemaining;
        }
    }
}
