using UnityEngine;

public class AgentMovement : MonoBehaviour
{
    public Transform agentCube;
    int xAxisValue;
    int zAxisValue;

    void Update()
    {
        float xAxisValue = agentCube.transform.position.x;
        float zAxisValue = agentCube.transform.position.z;


        if (Input.GetKeyDown("[8]"))
        {
            zAxisValue += 5;
        }

        if (Input.GetKeyDown("[5]"))
        {
            zAxisValue -= 5;
        }

        if (Input.GetKeyDown("[6]"))
        {
            xAxisValue += 5;
        }

        if (Input.GetKeyDown("[4]"))
        {
            xAxisValue -= 5;
        }

        agentCube.transform.position = new Vector3(transform.position.x + xAxisValue, 0, transform.position.z + zAxisValue);
    }
}