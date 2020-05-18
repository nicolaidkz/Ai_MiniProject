using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Repeater : MonoBehaviour
{
    public bool play;
    public static int counter;
    GameObject[] gos;

    // Start is called before the first frame update
    void Start()
    {
       counter = 0;
       StartCoroutine(RepeatAction());
    }

    IEnumerator RepeatAction()
    {
        while (play)
        {
            counter++;
            //DebugWorld();
            //SendNewMessage("SendSurroundings");
            SendNewMessage("Move");
            yield return new WaitForSeconds(2f);
        }

    }

    void SendNewMessage(string s)
    {
        gos = GameObject.FindGameObjectsWithTag("Avatar");
        
        for (var i = 0; i < gos.Length; i++)
        {
            gos[i].SendMessage(s, Coord.up);
        }
    }

    void DebugWorld()
    {
        string worldMapAscii = "";
        string[,] tmpWorldMap = Environment.worldMap;

        for (int y = 0; y < 28; y++)
        {
            worldMapAscii += "\n";

            for (int x = 0; x < 28; x++)
            {
                worldMapAscii += tmpWorldMap[x, y];
            }

        }

        Debug.Log(worldMapAscii);
    }

}

