using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObjectInfo : MonoBehaviour
{
    //public int colourMaterialIndex;
    public ObjectType type;
    //public Material material;

    public Coord coord;
    //
    [HideInInspector]
    public int mapIndex;
    [HideInInspector]
    public Coord mapCoord;

    protected bool dead;
    // Settings:
    protected float maxRot = 4;
    protected float maxScaleDeviation = .2f;
    protected float colVariationFactor = 0.15f;
    protected float minCol = .8f;

    public virtual void Init(Coord coord, System.Random spawnPrng)
    {
        this.coord = coord;
        transform.position = Environment.tileCentres[coord.x, coord.y];

        // Randomize rot/scale
        float rotY = (float)spawnPrng.NextDouble() * 360f;
        Quaternion rot = Quaternion.Euler(0, rotY, 0);

        // Randomize colour
        float col = Mathf.Lerp(minCol, 1, (float)spawnPrng.NextDouble());
        float r = col + ((float)spawnPrng.NextDouble() * 2 - 1) * colVariationFactor;
        float g = col + ((float)spawnPrng.NextDouble() * 2 - 1) * colVariationFactor;
        float b = col + ((float)spawnPrng.NextDouble() * 2 - 1) * colVariationFactor;

        for (int i = 0; i < this.transform.childCount; i++)
        {
            this.transform.GetChild(0).GetChild(i).GetComponent<MeshRenderer>().material.color = new Color(r, g, b);
        }

        this.transform.GetChild(0).SetPositionAndRotation(this.transform.position, rot);
    }

    protected virtual void Die(CauseOfDeath cause)
    {
        if (!dead)
        {
            dead = true;
            Environment.RegisterDeath (this);
            Destroy(gameObject);
        }
    }
}
