using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//will add components if object dont have them already
[RequireComponent(typeof(MeshFilter))]
[RequireComponent(typeof(MeshRenderer))]
[RequireComponent(typeof(MeshCollider))]

public class TileMap : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        BuildMesh();
    }

    void BuildMesh()
    {
        // Generate new mesh data
        Vector3[] vertices = new Vector3[4];
        int[] triangles = new int[2 * 3];
        Vector3[] normals = new Vector3[4];
        Vector2[] uv = new Vector2[4];





        // Create a new mesh and populate with the data
        Mesh mesh = new Mesh();
        mesh.vertices = vertices;
        mesh.triangles = triangles;
        mesh.normals = normals;

        // Assign our mesh to our filter/renderer/collider
        MeshFilter mesh_filter = GetComponent<MeshFilter>();
        MeshRenderer mesh_renderer = GetComponent<MeshRenderer>();
        MeshCollider mesh_collider = GetComponent<MeshCollider>();
    }

}
