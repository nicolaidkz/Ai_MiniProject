using UnityEngine;

public class FlyCamera : MonoBehaviour
{
    public int Speed = 50;
    void Update()
    {
        float xAxisValue = Input.GetAxis("Horizontal") * Speed;
        float zAxisValue = Input.GetAxis("Vertical") * Speed;
        float yValue = 0.0f;

        if (Input.GetAxis("Mouse ScrollWheel") > 0f)
        {
            yValue = -Speed*0.5f;
        }
        if (Input.GetAxis("Mouse ScrollWheel") < 0f)
        {
            yValue = Speed * 0.5f;
        }

        transform.position = new Vector3(transform.position.x + xAxisValue, transform.position.y + yValue, transform.position.z + zAxisValue);
    }
}