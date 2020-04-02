using System.Collections;
using UnityEngine;

public class TileMapMouse: MonoBehaviour
{
    Vector3 currentTileCoord;
    int x;
    int z;
    public Transform selectionCube;

    // Update is called once per frame
    void Update()
    {
        Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
        RaycastHit hitinfo;

        if (GetComponent<Collider>().Raycast( ray, out hitinfo, Mathf.Infinity))
        {
            gameObject.transform.InverseTransformPoint(hitinfo.point);
            x = Mathf.FloorToInt(hitinfo.point.x);
            z = Mathf.FloorToInt(hitinfo.point.z);

            currentTileCoord.x = x;
            currentTileCoord.z = z;

            selectionCube.transform.position = currentTileCoord;
        }
        else
        {
            
        }

        if (Input.GetMouseButtonDown(0))
        {
            Debug.Log("Tile: " + x + ", " + z);
        }
    }
}
