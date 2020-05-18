using System.Collections;
using System.Collections.Generic;
using TerrainGeneration;
using UnityEngine;
using System;

public class Environment : MonoBehaviour {

    const int mapRegionSize = 10;

    public int seed;

    [Header ("Populations")]
    public Population[] Populations;

    // Cached data:
    public static Vector3[, ] tileCentres;
    public static bool[, ] walkable;
    static int size;
    static List<Coord> walkableCoords;

    public static List<ObjectInfo> objects = new List<ObjectInfo>();

    static System.Random prng;
    TerrainGenerator.TerrainData terrainData;

    static Dictionary<ObjectType, Map> typeMaps;
    public static string[,] worldMap;

    void Start () {
        prng = new System.Random ();

        Init ();
        SpawnPopulations ();
    }

    public static void UpdateWorldMap()
    {
        var tre = GameObject.FindGameObjectsWithTag("Tree");
        var ava = GameObject.FindGameObjectsWithTag("Avatar");

        foreach (GameObject item in tre)
        {
            Coord tmpCoord = item.GetComponent<Trees>().coord;
            worldMap[tmpCoord.x+4, tmpCoord.y+4] = "T";
        }
        foreach (GameObject item in ava)
        {
            Coord tmpCoord = item.GetComponent<Avatar>().coord;
            worldMap[tmpCoord.x+4, tmpCoord.y+4] = "A";
        }

    }

    public static void RegisterMove(ObjectInfo entity, Coord from, Coord to)
    {
        typeMaps[entity.type].Move(entity, from, to);
    }

    public static void RegisterDeath(ObjectInfo entity)
    {
        typeMaps[entity.type].Remove(entity, entity.coord);
    }

    void Init () {
        var sw = System.Diagnostics.Stopwatch.StartNew ();

        var terrainGenerator = FindObjectOfType<TerrainGenerator> ();
        terrainData = terrainGenerator.Generate ();

        tileCentres = terrainData.tileCentres;
        walkable = terrainData.walkable;
        size = terrainData.size;

        worldMap = new string[terrainData.size+8, terrainData.size+8];

        for (int y = 0; y < terrainData.size + 8; y++)
        {
            for (int x = 0; x < terrainData.size + 8; x++)
            {
                worldMap[x,y] = "W";
            }
        }

        int numTypes = System.Enum.GetNames(typeof(ObjectType)).Length;

        //Init species maps
        typeMaps = new Dictionary<ObjectType, Map>();
        for (int i = 0; i < numTypes; i++)
        {
            ObjectType types = (ObjectType)(1 << i);
            typeMaps.Add(types, new Map(size, mapRegionSize));
        }

        walkableCoords = new List<Coord>();

        for (int y = 0; y < terrainData.size; y++)
        {
            for (int x = 0; x < terrainData.size; x++)
            {

                worldMap[x+4, y+4] = "X";

                if (walkable[x, y])
                {
                    walkableCoords.Add(new Coord(x, y));
                    worldMap[x+4, y+4] = "O";
                }
            }
        }

        Debug.Log ("Init time: " + sw.ElapsedMilliseconds);
    }

    void SpawnPopulations () {

        var spawnPrng = new System.Random (seed);
        var spawnCoords = new List<Coord> (walkableCoords);

        foreach (var pop in Populations) {
            var holder = new GameObject(pop.prefab.ToString() + " Holder").transform;
            for (int i = 0; i < pop.count; i++) {
                if (spawnCoords.Count == 0) {
                    Debug.Log ("Ran out of empty tiles to spawn initial population");
                    break;
                }
                int spawnCoordIndex = spawnPrng.Next (0, spawnCoords.Count);
                Coord coord = spawnCoords[spawnCoordIndex];
                spawnCoords.RemoveAt (spawnCoordIndex);

                // spawn entity
                var entity = Instantiate(pop.prefab, holder);
                entity.Init(coord, spawnPrng);
                entity.tag = entity.type.ToString();

                if (entity.tag == "FoodStore")
                {
                    worldMap[entity.coord.x+4, entity.coord.y+4] = "F";
                }
                if (entity.tag == "LumberMill")
                {
                    worldMap[entity.coord.x+4, entity.coord.y+4] = "L";
                }

                typeMaps[entity.type].Add (entity, coord);
            }
        }

        UpdateWorldMap();
    }


    [System.Serializable]
    public struct Population {
        public ObjectInfo prefab;
        public int count;
    }

}