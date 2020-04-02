using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//See in editor instead of only in play mode
[ExecuteInEditMode]

//will add components if object dont have them already
[RequireComponent(typeof(MeshFilter))]
[RequireComponent(typeof(MeshRenderer))]
[RequireComponent(typeof(MeshCollider))]

public class TileMap : MonoBehaviour
{
    public int size_x = 1000;
    public int size_z = 1000;
    public float tileSize = 1.0f;

    // Start is called before the first frame update
    void Start()
    {
        BuildMesh();
    }

    void BuildTexture()
    {
        int texWidth = 10;
        int texHeight = 10;
        Texture2D texture = new Texture2D(texWidth, texHeight);

        for (int y=0; y< texHeight; y++)
        {
            for (int x = 0; x < texWidth; x++)
            {
                Color c = new Color(Random.Range(0f, 1f), 0, 0);
                texture.SetPixel(x, y, c);
            }
        }
        texture.filterMode = FilterMode.Point;
        texture.wrapMode = TextureWrapMode.Clamp;
        texture.Apply();

        MeshRenderer mesh_renderer = GetComponent<MeshRenderer>();
        mesh_renderer.sharedMaterials[0].mainTexture = texture;

        Debug.Log("Done Texture");
    }

    public void BuildMesh()
    {

        int numTiles = size_x * size_z;
        int numTriangles = numTiles * 2;

        int vertsize_x = size_x + 1;
        int vertsize_z = size_z + 1;
        int numVerts = vertsize_x * vertsize_z;

        // Generate new mesh data
        Vector3[] vertices = new Vector3[numVerts];
        Vector3[] normals = new Vector3[numVerts];
        Vector2[] uv = new Vector2[numVerts];

        int[] triangles = new int[numTriangles * 3];

        int x, z;
        for(z=0; z < vertsize_z; z++)
        {
            for(x=0; x < vertsize_x; x++)
            {
                vertices[z * vertsize_x + x] = new Vector3(x * tileSize, 0, z * tileSize);
                normals[z * vertsize_x + x] = Vector3.up;
                uv[z * vertsize_x + x] = new Vector2((float)x / size_x, (float)z / size_z);
            }
        }
        Debug.Log("Done Verts");

        for (z = 0; z < size_z; z++)
        {
            for (x = 0; x < size_x; x++)
            {
                int squareindex = z * size_x + x;
                int triangleOffset = squareindex * 6;
                
                triangles[triangleOffset + 0] = z * vertsize_x + x +              0;
                triangles[triangleOffset + 1] = z * vertsize_x + x + vertsize_x + 0;
                triangles[triangleOffset + 2] = z * vertsize_x + x + vertsize_x + 1;
                
                triangles[triangleOffset + 3] = z * vertsize_x + x +              0;
                triangles[triangleOffset + 4] = z * vertsize_x + x + vertsize_x + 1;
                triangles[triangleOffset + 5] = z * vertsize_x + x +              1;
            }
        }
        Debug.Log("Done Triangles");

        // Create a new mesh and populate with the data
        Mesh mesh = new Mesh();
        mesh.vertices = vertices;
        mesh.triangles = triangles;
        mesh.normals = normals;
        mesh.uv = uv;

        // Assign our mesh to our filter/renderer/collider
        MeshFilter mesh_filter = GetComponent<MeshFilter>();
        MeshRenderer mesh_renderer = GetComponent<MeshRenderer>();
        MeshCollider mesh_collider = GetComponent<MeshCollider>();

        mesh_filter.mesh = mesh;
        mesh_collider.sharedMesh = mesh;
        Debug.Log("Done Mesh");

        BuildTexture();
    }

}

//Manually adding data
//vertices[0] = new Vector3(0, 0, 0);
//vertices[1] = new Vector3(1, 0, 0);
//vertices[2] = new Vector3(0, 0, -1);
//vertices[3] = new Vector3(1, 0, -1);

//triangles[0] = 0;
//triangles[1] = 3;
//triangles[2] = 2;

//triangles[3] = 0;
//triangles[4] = 1;
//triangles[5] = 3;

//normals[0] = Vector3.up;
//normals[1] = Vector3.up;
//normals[2] = Vector3.up;
//normals[3] = Vector3.up;

//uv[0] = new Vector2(0, 0);
//uv[1] = new Vector2(1, 0);
//uv[2] = new Vector2(0, 1);
//uv[3] = new Vector2(1, 1);
