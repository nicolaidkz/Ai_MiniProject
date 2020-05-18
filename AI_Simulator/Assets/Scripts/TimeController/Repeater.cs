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
            yield return new WaitForSeconds(1f);
        }

    }

    void SendNewMessage(string s)
    {
        gos = GameObject.FindGameObjectsWithTag("Avatar");
        Coord corRNG = Coord.invalid;

        for (var i = 0; i < gos.Length; i++)
        {
            int numRNG = Random.Range(0, 4);
            if (numRNG == 0)
            {
                corRNG = Coord.up;
            }
            else if (numRNG == 1)
            {
                corRNG = Coord.down;
            }
            else if (numRNG == 2)
            {
                corRNG = Coord.right;
            }
            else if (numRNG == 3)
            {
                corRNG = Coord.left;
            }
     
            gos[i].SendMessage(s, corRNG);
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

